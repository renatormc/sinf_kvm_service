from flask import Blueprint, jsonify, request, abort, make_response
from helpers import libvirt

api = Blueprint('api', __name__)


@api.route("/")
def index():
    return "VM teste"


@api.route("/save_usbs")
def save_usbs():
    usbs = libvirt.list_usbs()
    return "VM teste"