from helpers import libvirt
import config
import json
from uuid import uuid4

def snapshot_current_devices():
    disks = libvirt.list_disks()
    usbs = libvirt.list_usbs()
    random_id = uuid4()
    path = config.files_folder / f"{random_id}.json"
    data = {
        'disks': disks,
        'usbs': usbs
    }
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return random_id


def list_new_devices(random_id):
    path = config.files_folder / f"{random_id}.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    path.unlink()
    disks = libvirt.list_disks()
    usbs = libvirt.list_usbs()

    new_disks = []
    for disk in disks:
        if disk not in data['disks']:
            new_disks.append(disk)

    new_usbs = []
    for usb in usbs:
        if usb not in data['usbs']:
            new_usbs.append(usb)
    return {
        'disks': new_disks,
        'usb': new_usbs
    }
