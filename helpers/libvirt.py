from subprocess import check_output, CalledProcessError, PIPE, Popen
import subprocess
from typing import List, TypedDict
import re
import config
from uuid import uuid4
from blkinfo import BlkDiskInfo
import json
import xml.etree.ElementTree as ET


class UsbType(TypedDict):
    bus: str
    device: str
    id: str
    name: str


class VmType(TypedDict):
    id: str
    name: str
    state: str


class DiskType(TypedDict):
    vendor: str
    label: str
    model: str
    name: str
    kname: str


def execute(args: list[str]) -> tuple[bytes, bytes]:
    print(" ".join(args))
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    std_out, std_err = p.communicate()
    if p.returncode != 0:
        return std_out, std_err
    return std_out, std_err


def read_fixed_usbs() -> list[UsbType]:
    path = config.fixed_usbs_filepath
    data: list[UsbType] = []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


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


def list_usbs(filter_fixed=False) -> list[UsbType]:
    fixed_usbs = read_fixed_usbs() if filter_fixed else []
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
            if not filter_fixed or not dev in fixed_usbs:
                devs.append(dev)
    return devs


def save_fixed_usb():
    usbs = list_usbs(filter_fixed=False)
    path = config.fixed_usbs_filepath
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(usbs, indent=4, ensure_ascii=False))


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


def get_attached_usbs(vm: str) -> list[str]:
    out = subprocess.getoutput(f"virsh -c qemu:///system dumpxml {vm}")
    root = ET.fromstring(out)
    usbs: list[str] = []
    for hostdev in root.findall(".//hostdev"):
        if hostdev.attrib['type'] == "usb":
            source = hostdev.find(".//source")
            if source is None:
                continue
            vendor = source.find(".//vendor").attrib['id'][2:]
            if vendor is None:
                continue
            product = source.find(".//product").attrib['id'][2:]
            id = f"{vendor}:{product}"
            usbs.append(id)
    return usbs