from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.uploaded_by_schema import (
    UploadCreateSchema,
    UploadReadSchema,
    UploadUpdateSchema,
)
from flask import g
from app.core.guards import require_auth

from app.crud.uploads_crud import (
    create_upload_for_user,
    get_upload_by_song_id,
    get_upload_by_song_id_with_private_guard,
    set_upload_private_for_owner,
    list_my_uploads_with_song,
)

uploads_bp = Blueprint("uploads", __name__)

upload_create_schema = UploadCreateSchema()
upload_read_schema = UploadReadSchema()
upload_update_schema = UploadUpdateSchema()





@uploads_bp.post("/uploads")
@require_auth
def create_upload():
    user_id = g.user_id


    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    try:
        data = upload_create_schema.load(payload)
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "messages": e.messages}), 422

    # DB via CRUD (pas de commit ici)
    upload = create_upload_for_user(
        db.session,
        user_id=user_id,
        song_id=data["song_id"],
        private=data["private"],
    )

    return jsonify(upload_read_schema.dump(upload)), 201


@uploads_bp.patch("/uploads/<int:song_id>")
@require_auth
def patch_upload(song_id: int):
    user_id = g.user_id

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    try:
        data = upload_update_schema.load(payload)
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "messages": e.messages}), 422

    if "private" not in data:
        return jsonify({"error": "ValidationError", "message": "Provide 'private' (true/false)."}), 422

    upload = set_upload_private_for_owner(
        db.session,
        user_id=user_id,
        song_id=song_id,
        private=data["private"],
    )

    return jsonify(upload_read_schema.dump(upload)), 200


@uploads_bp.get("/uploads/<int:song_id>")
@require_auth
def get_upload(song_id: int):
    user_id = g.user_id
    upload = get_upload_by_song_id_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=user_id,
    )
    return jsonify(upload_read_schema.dump(upload)), 200


@uploads_bp.get("/uploads/me")
@require_auth
def get_my_uploads():
    user_id = g.user_id

    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 50, type=int)
    limit = max(1, min(limit, 100))

    items = list_my_uploads_with_song(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    return jsonify({
        "count": len(items),
        "items": items,
    }), 200
