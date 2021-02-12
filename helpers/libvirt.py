from subprocess import check_output
from typing import List
import re

class VM:
    def __init__(self):
        self.id = None
        self.name = None
        self.state = None

    def __repr__(self):
        return self.name



def list_running_vms() -> List[VM]:
    res = check_output(["virsh", "list"], universal_newlines=True).strip()
    items = [line.split() for line in res.split("\n")]
    ret = []
    for item in items[2:]:
        obj = VM()
        obj.id = item[0]
        obj.name = item[1]
        obj.state = item[2]
        ret.append(obj)
    return ret


def list_usbs():
    res = check_output(["lsusb"], universal_newlines=True).strip()
    lines = res.split("\n")
    devs = []
    reg = re.compile(r'Bus (\d+) Device (\d+): ID (\S+) (.*)')
    for line in lines:
        res = reg.search(line)
        if res:
            dev = {
                'bus': res.group(1),
                'device': res.group(2),
                'id': res.group(3),
                'name': res.group(4),
            }
            devs.append(dev)
    return devs