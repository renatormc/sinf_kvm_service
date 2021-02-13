from flask import Blueprint, jsonify, request, abort, make_response
from helpers import libvirt, api_helpers

api = Blueprint('api', __name__)


@api.route("/test")
def test():
    return "VM teste"


@api.route("/list-running-vms")
def list_running_vms():
    vms = libvirt.list_running_vms()
    return jsonify(vms)


@api.route("/snapshot-devices")
def save_devices():
    id = api_helpers.snapshot_current_devices()
    return jsonify({
        "id": id
    })


@api.route("/new-devices/<id>")
def new_devices(id):
    devs = api_helpers.list_new_devices(id)
    return jsonify(devs)


@api.route("/attach-usb/<id>/<vm>")
def attach_usb(id, vm):
    libvirt.attach_detach_usb(id, vm, action="attach")
    return "ok"


@api.route("/detach-usb/<id>/<vm>")
def detach_usb(id, vm):
    libvirt.attach_detach_usb(id, vm, action="detach")
    return "ok"


@api.route("/attach-disk/<name>/<vm>")
def attach_disk(name, vm):
    libvirt.attach_detach_disk(name, vm, action="attach")
    return "ok"


@api.route("/detach-disk/<name>/<vm>")
def detach_disk(name, vm):
    libvirt.attach_detach_disk(name, vm, action="detach")
    return "ok"
