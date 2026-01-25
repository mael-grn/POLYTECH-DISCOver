from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.user_schema import UserCreateSchema

from app.crud.users_crud import (
    get_user_by_id,
    create_user_row,
    list_users_basic,
)
from flask import g
from app.core.guards import require_auth
users_bp = Blueprint("users", __name__)
user_create_schema = UserCreateSchema()





@users_bp.get("/users/me")
@require_auth
def get_me():
    user_id = g.user_id


    user = get_user_by_id(db.session, user_id=user_id)
    if user is None:
        return jsonify({"error": "NotFound", "message": f"User {user_id} not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "name": getattr(user, "name", None),
        "email": getattr(user, "email", None),
        "created_at": getattr(user, "created_at", None),
    }), 200


@users_bp.post("/users")
def create_user():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON"}), 400

    try:
        data = user_create_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422


    user = create_user_row(
        db.session,
        name=data["name"],
        password=data["password"],
        email=data.get("email"),
    )


    return jsonify({
        "user_id": user.user_id,
        "username": getattr(user, "username", getattr(user, "name", None)),
        "name": getattr(user, "name", None),
        "email": getattr(user, "email", None),
    }), 201


@users_bp.get("/users")
def list_users():
    limit = request.args.get("limit", 50, type=int)
    limit = max(1, min(limit, 200))

    users = list_users_basic(db.session, limit=limit)

    return jsonify({
        "count": len(users),
        "items": [
            {
                "user_id": u.user_id,
                "name": getattr(u, "name", None),
                "email": getattr(u, "email", None),
            }
            for u in users
        ]
    }), 200

@users_bp.patch("/users/me")
@require_auth
def update_me():
    user_id = g.user_id

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON"}), 400

    allowed_fields = {"name", "email", "password"}
    data = {k: v for k, v in payload.items() if k in allowed_fields}

    if not data:
        return jsonify({
            "error": "ValidationError",
            "message": "Provide at least one of: name, email, password"
        }), 422

    user = get_user_by_id(db.session, user_id=user_id)
    if user is None:
        return jsonify({"error": "NotFound"}), 404

    from app.crud.users_crud import update_user

    user = update_user(
        db.session,
        user=user,
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password"),
    )

    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
    }), 200