from flask import Blueprint, jsonify, request
from app.api.deps import get_request_user_id
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserCreateSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint("users", __name__)
user_create_schema = UserCreateSchema()

@users_bp.get("/users/me")
def get_me():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    user = db.session.get(User, user_id)
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

    user = User(
        name=data["name"],
        email=data.get("email")
    )
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "IntegrityError",
        "message": "User already exists (name or email must be unique).",
                        "details": str(getattr(e, "orig", e))}), 409

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email
    }), 201

@users_bp.get("/users")
def list_users():
    # dev: limite pour éviter de dump trop
    limit = request.args.get("limit", 50, type=int)
    limit = max(1, min(limit, 200))

    users = db.session.query(User).order_by(User.user_id.asc()).limit(limit).all()
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