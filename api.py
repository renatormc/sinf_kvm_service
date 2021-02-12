from flask import Blueprint, jsonify, request, abort, make_response

api = Blueprint('api', __name__)


@api.route("/")
def index():
    return "Teste"