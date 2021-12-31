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


def list_usbs(filter_excluded=False) -> list[UsbType]:
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
            if not filter_excluded or not dev in config.local_config['exclude_usb']:
                devs.append(dev)
    return devs


def list_disks(filter_excluded=False) -> list[DiskType]:
    myblkd = BlkDiskInfo()
    disks = myblkd.get_disks()
    disks = [{
        'vendor': disk['vendor'],
        'label': disk['label'],
        'model': disk['model'],
        'name': disk['name'],
        'kname': disk['kname'],
    } for disk in disks]
    if filter_excluded:
        disks = [d for d in disks if d not in config.local_config['exclude_disk']]
    return disks


def save_exclude_devices():
    usbs = list_usbs(filter_excluded=False)
    disks = list_disks(filter_excluded=False)
    with config.config_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data['exclude_usb'] = usbs
    data['exclude_disk'] = disks
    with config.config_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


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


def get_attached_disks(vm: str) -> list[str]:
    out = subprocess.getoutput(f"virsh -c qemu:///system dumpxml {vm}")
    root = ET.fromstring(out)
    disks: list[str] = []
    for disk in root.findall(".//disk"):
        if disk.attrib['type'] == "block":
            source = disk.find(".//source")
            if source is None:
                continue
            dev = source.attrib['dev'].split("/")[-1]
            disks.append(dev)
    return disks
