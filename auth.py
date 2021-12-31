from flask import g, request, abort, make_response, jsonify
from functools import wraps
from datetime import date, datetime
import config


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_token():
            abort(make_response(jsonify(message="Unauthorized"), 401))
        return f(*args, **kwargs)
    return decorated_function


def check_token() -> bool:
    try:
        value = request.headers.get(
            'Authorization') or request.cookies.get('Authorization')
        print(value)
        return value == config.local_config['password']
    except (AttributeError):
        return False
