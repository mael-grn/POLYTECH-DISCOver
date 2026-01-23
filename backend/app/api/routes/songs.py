from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.song_schema import SongCreateSchema, SongReadSchema
from app.schemas.song_list_schema import SongListItemSchema


from app.crud.songs_crud import (
    create_song_row,
    get_song_with_private_guard,
    list_songs_with_upload_guard_and_search,
    list_my_songs_with_search,
    delete_uploaded_song_for_owner,
)

songs_bp = Blueprint("songs", __name__)

song_create_schema = SongCreateSchema()
song_read_schema = SongReadSchema()
songs_list_schema = SongListItemSchema(many=True)
songs_me_schema = SongListItemSchema(many=True)


def _require_user_id():
    user_id = get_request_user_id()
    if user_id is None:
        return None, (jsonify({"error": "Unauthorized", "message": "Missing X-User-Id"}), 401)
    return user_id, None



@songs_bp.post("/songs")
def create_song():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    try:
        data = song_create_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422


    song = create_song_row(db.session, data=data)

    return jsonify(song_read_schema.dump(song)), 201



@songs_bp.get("/songs/<int:song_id>")
def get_song(song_id: int):
    maybe_user_id = get_request_user_id()


    song = get_song_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=maybe_user_id,
        should_touch_history=True,
    )

    return jsonify(song_read_schema.dump(song)), 200



@songs_bp.get("/songs")
def list_songs():
    maybe_user_id = get_request_user_id()

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    skip = max(skip, 0)
    limit = max(1, min(limit, 100))

    search = (request.args.get("q", "") or "").strip()
    mode = (request.args.get("mode", "any") or "any").strip().lower()  # any | all

    if search and len(search) > 120:
        return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
    if mode not in ("any", "all"):
        return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422

    items = list_songs_with_upload_guard_and_search(
        db.session,
        maybe_user_id=maybe_user_id,
        skip=skip,
        limit=limit,
        search=search,
        mode=mode,
    )

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_list_schema.dump(items),
    }), 200



@songs_bp.get("/songs/me")
def list_my_songs():
    user_id, err = _require_user_id()
    if err:
        return err

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    skip = max(skip, 0)
    limit = max(1, min(limit, 100))

    search = (request.args.get("q", "") or "").strip()
    mode = (request.args.get("mode", "any") or "any").strip().lower()

    if search and len(search) > 120:
        return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
    if mode not in ("any", "all"):
        return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422

    items = list_my_songs_with_search(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
        search=search,
        mode=mode,
    )

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_me_schema.dump(items),
    }), 200



@songs_bp.delete("/songs/<int:song_id>")
def delete_song(song_id: int):
    user_id, err = _require_user_id()
    if err:
        return err

    delete_uploaded_song_for_owner(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    return jsonify({"status": "deleted", "song_id": song_id}), 200
