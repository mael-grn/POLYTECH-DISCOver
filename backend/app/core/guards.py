from functools import wraps
from flask import request, jsonify, g
from app.core.jwt_auth import verify_access_token, COOKIE_NAME

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.cookies.get(COOKIE_NAME)
        if not token:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = verify_access_token(token)
        if user_id is None:
            return jsonify({"error": "Unauthorized"}), 401

        g.user_id = int(user_id)
        return fn(*args, **kwargs)
    return wrapper

from functools import wraps
from flask import g

def optional_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.cookies.get(COOKIE_NAME)

        if not token:
            g.user_id = None
            return fn(*args, **kwargs)

        user_id = verify_access_token(token)
        if user_id is None:
            g.user_id = None
            return fn(*args, **kwargs)

        g.user_id = int(user_id)
        return fn(*args, **kwargs)

    return wrapper
