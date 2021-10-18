from flask import Blueprint, jsonify, request, abort, make_response
from helpers import libvirt, api_helpers
from mippae_libs.auth import jwt_required

api = Blueprint('api', __name__)


@api.route("/test")
@jwt_required
def test():
    return "VM teste"


@api.route("/list-running-vms")
@jwt_required
def list_running_vms():
    vms = libvirt.list_running_vms()
    return jsonify(vms)


@api.route("/snapshot-devices")
@jwt_required
def save_devices():
    id = api_helpers.snapshot_current_devices()
    return jsonify({
        "id": id
    })


@api.route("/new-devices/<id>")
@jwt_required
def new_devices(id: str):
    devs = api_helpers.list_new_devices(id)
    return jsonify(devs)


@api.route("/attach-usb/<id>/<vm>")
@jwt_required
def attach_usb(id: str, vm: str):
    std_out, std_err = libvirt.attach_detach_usb(id, vm, action="attach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/detach-usb/<id>/<vm>")
@jwt_required
def detach_usb(id: str, vm: str):
    std_out, std_err = libvirt.attach_detach_usb(id, vm, action="detach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/attach-disk/<name>/<vm>")
@jwt_required
def attach_disk(name: str, vm: str):
    std_out, std_err = libvirt.attach_detach_disk(name, vm, action="attach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())


@api.route("/detach-disk/<name>/<vm>")
@jwt_required
def detach_disk(name: str, vm: str):
    std_out, std_err = libvirt.attach_detach_disk(name, vm, action="detach")
    if std_err:
        abort(jsonify(message=std_err.decode()))
    return jsonify(message=std_out.decode())
