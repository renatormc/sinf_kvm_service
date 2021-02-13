from helpers import libvirt
from blkinfo import BlkDiskInfo
from pprint import pprint
from helpers import api_helpers


id = api_helpers.snapshot_current_devices()
input("Pressione algo")
devices = api_helpers.list_new_devices(id)
pprint(devices)