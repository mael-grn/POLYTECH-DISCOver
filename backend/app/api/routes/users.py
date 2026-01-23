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

users_bp = Blueprint("users", __name__)
user_create_schema = UserCreateSchema()


def _require_user_id():
    user_id = get_request_user_id()
    if user_id is None:
        return None, (jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401)
    return user_id, None


@users_bp.get("/users/me")
def get_me():
    user_id, err = _require_user_id()
    if err:
        return err

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
