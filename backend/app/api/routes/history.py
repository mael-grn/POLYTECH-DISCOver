from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.models.history import History
from app.schemas.history_schema import HistoryCreateSchema, HistoryReadSchema

history_bp = Blueprint("history", __name__)

history_create_schema = HistoryCreateSchema()
history_read_schema = HistoryReadSchema()
history_list_schema = HistoryReadSchema(many=True)


@history_bp.post("/history")
def create_or_touch_history():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    try:
        data = history_create_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    song_id = data["song_id"]
    now = datetime.now(timezone.utc)

    row = (
        db.session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .first()
    )

    if row is None:
        row = History(user_id=user_id, song_id=song_id, date=now, last_research=now)
        db.session.add(row)
    else:
        row.last_research = now

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "DatabaseError", "message": "Failed to write history"}), 500

    return jsonify(history_read_schema.dump(row)), 201


@history_bp.get("/history")
def list_history():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    skip = max(skip, 0)
    limit = max(1, min(limit, 100))

    rows = (
        db.session.query(History)
        .filter(History.user_id == user_id)
        .order_by(History.last_research.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(rows),
        "items": history_list_schema.dump(rows),
    }), 200


@history_bp.delete("/history")
def clear_history():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    try:
        deleted = (
            db.session.query(History)
            .filter(History.user_id == user_id)
            .delete(synchronize_session=False)
        )
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "DatabaseError", "message": "Failed to clear history"}), 500

    return jsonify({"status": "cleared", "deleted": deleted}), 200

@history_bp.delete("/history/<int:song_id>")
def delete_history_song(song_id: int):
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({
            "error": "Unauthorized",
            "message": "Missing X-User-Id (dev auth)"
        }), 401

    history = (
        db.session.query(History)
        .filter(
            History.user_id == user_id,
            History.song_id == song_id
        )
        .first()
    )

    if history is None:
        return jsonify({
            "error": "NotFound",
            "message": "Song not found in history"
        }), 404

    try:
        db.session.delete(history)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "DatabaseError",
            "message": "Failed to delete history entry"
        }), 500

    return jsonify({
        "status": "deleted",
        "song_id": song_id
    }), 200