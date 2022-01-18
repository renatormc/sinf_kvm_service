from flask import Blueprint, jsonify, request, abort, make_response
from helpers import libvirt, api_helpers
from auth import auth_required
import config

api = Blueprint('api', __name__)


@api.route("/test")
@auth_required
def test():
    return "VM teste"


@api.route("/list-running-vms")
@auth_required
def list_running_vms():
    vms = libvirt.list_running_vms()
    return jsonify(vms)


@api.route("/usbs")
@auth_required
def usbs():
    usbs = libvirt.list_usbs(filter_excluded=True)
    return jsonify(usbs)


@api.route("/disks")
@auth_required
def disks():
    disks = libvirt.list_disks(filter_excluded=True)
    return jsonify(disks)


@api.route("/attached-usbs/<vm>")
@auth_required
def attached_usbs(vm: str):
    usbs = libvirt.get_attached_usbs(vm)
    return jsonify(usbs)

@api.route("/attached-disks/<vm>")
@auth_required
def attached_disks(vm: str):
    usbs = libvirt.get_attached_disks(vm)
    return jsonify(usbs)


@api.route("/snapshot-devices")
@auth_required
def save_devices():
    id = api_helpers.snapshot_current_devices()
    return jsonify({
        "id": id
    })


@api.route("/new-devices/<id>")
@auth_required
def new_devices(id: str):
    devs = api_helpers.list_new_devices(id)
    return jsonify(devs)


@api.route("/attach-usb/<id>/<vm>")
@auth_required
def attach_usb(id: str, vm: str):
    std_out, std_err = libvirt.attach_detach_usb(id, vm, action="attach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/detach-usb/<id>/<vm>")
@auth_required
def detach_usb(id: str, vm: str):
    std_out, std_err = libvirt.attach_detach_usb(id, vm, action="detach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/attach-disk/<name>/<vm>")
@auth_required
def attach_disk(name: str, vm: str):
    std_out, std_err = libvirt.attach_detach_disk(name, vm, action="attach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/detach-disk/<name>/<vm>")
@auth_required
def detach_disk(name: str, vm: str):
    std_out, std_err = libvirt.attach_detach_disk(name, vm, action="detach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())



@api.route("/set-desktop/<int:number>")
@auth_required
def set_desktop(number: int):
    api_helpers.set_desktop(number)
    return jsonify({"msg": "ok"})