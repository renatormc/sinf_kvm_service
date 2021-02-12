from flask import Blueprint, jsonify, request, abort, make_response
from helpers import libvirt

api = Blueprint('api', __name__)


@api.route("/")
def index():
    return "VM teste"


@api.route("/list-running-vms")
def list_running_vms():
    return ""


@api.route("/save_current_usbs")
def save_current_usbs():
    return ""


@api.route("/list-new-usbs")
def list_new_usbs():
    return ""


@api.route("/attach-usb")
def attach_usb():
    return ""
