from subprocess import check_output, CalledProcessError, PIPE, Popen
from typing import List, TypedDict
import re
import config
from uuid import uuid4
from blkinfo import BlkDiskInfo


def execute(args: list[str]) -> tuple[bytes, bytes]:
    print(" ".join(args))
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    std_out, std_err = p.communicate()
    if p.returncode != 0:
        return std_out, std_err
    return std_out, std_err


class VmType(TypedDict):
    id: str
    name: str
    state: str


def list_running_vms() -> list[VmType]:
    res = check_output(["virsh", "-c", "qemu:///system",
                        "list"], universal_newlines=True).strip()
    items = [line.split() for line in res.split("\n")]
    ret = []
    for item in items[2:]:
        obj: VmType = {
            'id': item[0],
            'name': item[1],
            'state': item[2]
        }
        ret.append(obj)
    return ret


class UsbType(TypedDict):
    bus: str
    device: str
    id: str
    name: str


def list_usbs() -> list[UsbType]:
    res = check_output(["lsusb"], universal_newlines=True).strip()
    lines = res.split("\n")
    devs: list[UsbType] = []
    reg = re.compile(r'Bus (\d+) Device (\d+): ID (\S+) (.*)')
    for line in lines:
        resreg = reg.search(line)
        if resreg:
            dev: UsbType = {
                'bus': resreg.group(1) or "",
                'device': resreg.group(2) or "",
                'id': resreg.group(3) or "",
                'name': resreg.group(4) or "",
            }
            devs.append(dev)
    return devs


class DiskType(TypedDict):
    vendor: str
    label: str
    model: str
    name: str
    kname: str


def list_disks() -> list[DiskType]:
    myblkd = BlkDiskInfo()
    # filters = {
    #     'tran': 'usb'
    # }
    disks = myblkd.get_disks()
    disks = [{
        'vendor': disk['vendor'],
        'label': disk['label'],
        'model': disk['model'],
        'name': disk['name'],
        'kname': disk['kname'],
    } for disk in disks]
    return disks


def attach_detach_usb(id: str, vm: str, action: str = "attach"):
    vendor, prod = id.split(":")
    xml = f"""<hostdev mode='subsystem' type='usb' managed='yes'>
<source>
<vendor id='0x{vendor}'/>
<product id='0x{prod}'/>
</source>
</hostdev>"""
    print(xml)
    random_id = uuid4()
    tempfile = config.TEMPFOLDER / f"{random_id}.xml"
    tempfile.write_text(xml)
    try:
        res = execute(['virsh', '-c', 'qemu:///system', f"{action}-device",
                       vm, '--file', str(tempfile)])
    finally:
        tempfile.unlink()
    return res


def attach_detach_disk(name: str, vm: str, action="attach"):
    args = ['virsh', '-c', 'qemu:///system',
            f"{action}-disk", vm, f"/dev/{name}"]
    if action == "attach":
        args.append("vdc")
    return execute(args)
