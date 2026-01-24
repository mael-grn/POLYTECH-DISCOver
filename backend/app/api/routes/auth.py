from flask import Blueprint, request, jsonify, make_response, current_app

from app.extensions import db
from app.crud.users_crud import (
    authenticate_user,
    get_user_by_id,
    user_public_dict,
)
from app.core.jwt_auth import create_access_token, verify_access_token, COOKIE_NAME

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "BadRequest", "message": "email and password required"}), 400

    user = authenticate_user(db.session, email=email, password=password)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    token = create_access_token(user_id=user.user_id)

    resp = make_response(jsonify({"ok": True}), 200)
    resp.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=False,       # mets True en prod HTTPS
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

    # On passe par le CRUD
    user = get_user_by_id(db.session, user_id=int(user_id))
    if not user:
        # Token valide mais user supprimé / incohérent
        return jsonify({"logged_in": False}), 200

    return jsonify({
        "logged_in": True,
        "user": user_public_dict(user),
    }), 200
