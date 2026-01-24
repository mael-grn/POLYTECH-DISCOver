from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import check_password_hash

from app.extensions import db
from app.crud.user_crud import get_user_by_email
from app.core.jwt_auth import create_access_token, verify_access_token, COOKIE_NAME

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({
            "error": "BadRequest",
            "message": "email and password required"
        }), 400

    user = get_user_by_email(db.session, email=email)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Unauthorized"}), 401

    token = create_access_token(user_id=user.id)

    resp = make_response(jsonify({"ok": True}), 200)
    resp.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=int(current_app.config["JWT_EXP_SECONDS"]),
        path="/",
    )
    return resp


@auth_bp.post("/auth/logout")
def logout():
    resp = make_response(jsonify({"ok": True}), 200)
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp


@auth_bp.get("/auth/me")
def me():
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return jsonify({"logged_in": False}), 200

    user_id = verify_access_token(token)
    if user_id is None:
        return jsonify({"logged_in": False}), 200

    return jsonify({
        "logged_in": True,
        "user_id": user_id
    }), 200
