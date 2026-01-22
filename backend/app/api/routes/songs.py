from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db
from app.models.song import Song
from app.schemas.song_schema import SongCreateSchema, SongReadSchema
from sqlalchemy.exc import SQLAlchemyError
from app.api.deps import get_request_user_id
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from app.models.uploaded_by import UploadedBy
from app.schemas.song_list_schema import SongListItemSchema
import re
from app.services.history_service import touch_history
from app.services.search_service import apply_rich_search
from app.models.history import History


songs_bp = Blueprint("songs", __name__)

song_create_schema = SongCreateSchema()
song_read_schema = SongReadSchema()
songs_read_schema = SongReadSchema(many=True)
songs_list_schema = SongListItemSchema(many=True)
songs_me_schema = SongListItemSchema(many=True)


@songs_bp.post("/songs")
def create_song():
    schema_song = request.get_json(silent=True)
    if schema_song is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    try:
        data = song_create_schema.load(schema_song)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    song = Song(**data)

    db.session.add(song)
    db.session.commit()

    return jsonify(song_read_schema.dump(song)), 201

@songs_bp.get("/songs/<int:song_id>")
def get_song(song_id: int):
    user_id = get_request_user_id()

    song = db.session.get(Song, song_id)
    if song is None:
        return jsonify({"error": "NotFound", "message": f"Song {song_id} not found"}), 404

    upload = (
        db.session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )

    if upload is not None and upload.private:
        if user_id is None:
            return jsonify({"error": "Forbidden", "message": "Private song"}), 403
        if upload.user_id != user_id:
            return jsonify({"error": "Forbidden", "message": "Private song"}), 403
    if user_id is not None:
        try:
            touch_history(user_id, song_id)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    return jsonify(song_read_schema.dump(song)), 200

@songs_bp.get("/songs")
def list_songs():
    user_id = get_request_user_id()

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    skip = max(skip, 0)
    limit = max(1, min(limit, 100))

    q = (
        db.session.query(Song, UploadedBy)
        .outerjoin(UploadedBy, UploadedBy.song_id == Song.song_id)
    )
    search = request.args.get("q", "").strip()
    mode = request.args.get("mode", "any").strip().lower()  # any | all

    if search:
        if len(search) > 120:
            return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
        if mode not in ("any", "all"):
            return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422
        if search.isdigit():
            q = q.filter(Song.song_id == int(search))
        else:
            q = apply_rich_song_search(q, search, mode=mode)

        q = apply_rich_song_search(q, search, mode=mode)

    if user_id is None:
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),
                UploadedBy.private.is_(False),
            )
        )
    else:
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),
                UploadedBy.private.is_(False),
                UploadedBy.user_id == user_id,
            )
        )

    rows = (
        q.order_by(Song.song_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = []
    for song, upload in rows:
        data = {
            # Champs Song
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_duration_ms": getattr(song, "song_duration_ms", None),
            "song_popularity": getattr(song, "song_popularity", None),
            "acousticness": getattr(song, "acousticness", None),
            "danceability": getattr(song, "danceability", None),
            "energy": getattr(song, "energy", None),

            # Upload info (ou None si dataset)
            "upload": None if upload is None else {
                "user_id": upload.user_id,
                "private": upload.private,
                "date": upload.date,
            }
        }
        items.append(data)

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_list_schema.dump(items),
    }), 200

def apply_rich_song_search(query, search: str, mode: str = "any"):
    """
    mode:
      - "any" : au moins un token match (OR)
      - "all" : tous les tokens doivent match (AND)
    """
    tokens = [t for t in re.split(r"\s+", search.strip()) if t]
    if not tokens:
        return query

    if len(tokens) > 6:
        tokens = tokens[:6]

    searchable_cols = [Song.song_name]

    per_token_conditions = []
    for tok in tokens:
        like = f"%{tok}%"
        per_token_conditions.append(or_(*[col.ilike(like) for col in searchable_cols]))

    if mode == "all":
        return query.filter(and_(*per_token_conditions))
    return query.filter(or_(*per_token_conditions))

@songs_bp.get("/songs/me")
def list_my_songs():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    skip = max(skip, 0)
    limit = max(1, min(limit, 100))

    q = (
        db.session.query(Song, UploadedBy)
        .join(UploadedBy, UploadedBy.song_id == Song.song_id)
        .filter(UploadedBy.user_id == user_id)
    )

    search = request.args.get("q", "").strip()
    mode = request.args.get("mode", "any").strip().lower()
    if search:
        if len(search) > 120:
            return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
        if mode not in ("any", "all"):
            return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422
        q = apply_rich_search(q, search, columns=[Song.song_name], mode=mode)

    rows = (
        q.order_by(UploadedBy.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = []
    for song, upload in rows:
        items.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_duration_ms": getattr(song, "song_duration_ms", None),
            "song_popularity": getattr(song, "song_popularity", None),
            "acousticness": getattr(song, "acousticness", None),
            "danceability": getattr(song, "danceability", None),
            "energy": getattr(song, "energy", None),
            "upload": {
                "user_id": upload.user_id,
                "private": upload.private,
                "date": upload.date,
            }
        })

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_me_schema.dump(items),
    }), 200

@songs_bp.delete("/songs/<int:song_id>")
def delete_song(song_id: int):
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({
            "error": "Unauthorized",
            "message": "Missing X-User-Id (dev auth)"
        }), 401

    upload = (
        db.session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )
    if upload is None:
        return jsonify({
            "error": "Forbidden",
            "message": "This song is part of the dataset and cannot be deleted"
        }), 403

    if upload.user_id != user_id:
        return jsonify({
            "error": "Forbidden",
            "message": "Only the uploader can delete this song"
        }), 403

    song = db.session.get(Song, song_id)
    if song is None:
        return jsonify({
            "error": "NotFound",
            "message": f"Song {song_id} not found"
        }), 404

    try:
        db.session.query(History)\
            .filter(History.song_id == song_id)\
            .delete(synchronize_session=False)

        db.session.delete(upload)
        db.session.delete(song)

        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "DatabaseError",
            "message": "Failed to delete song"
        }), 500

    return jsonify({
        "status": "deleted",
        "song_id": song_id
    }), 200
