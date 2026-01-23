# app/api/routes/history.py
from __future__ import annotations
from app.api.deps import *
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.services.history_service import _require_user_id
from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.history_schema import HistoryCreateSchema, HistoryReadSchema
from app.crud.history_crud import (
    create_or_touch,
    list_for_user,
    get_one_for_user,
    delete_all_for_user,
    delete_one_for_user,
)

history_bp = Blueprint("history", __name__)

# Schemas
history_create_schema = HistoryCreateSchema()
history_read_schema = HistoryReadSchema()
history_list_schema = HistoryReadSchema(many=True)


@history_bp.post("/history")
def create_history():
    user_id, err = _require_user_id()
    if err:
        return err

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            "error": "InvalidJSON",
            "message": "Request body must be valid JSON"
        }), 400

    try:
        data = history_create_schema.load(payload)
    except ValidationError as e:
        return jsonify({
            "error": "ValidationError",
            "messages": e.messages
        }), 422

    row = create_or_touch(
        db.session,
        user_id=user_id,
        song_id=data["song_id"],
    )

    return jsonify(history_read_schema.dump(row)), 201



@history_bp.get("/history")
def list_history():
    user_id, err = _require_user_id()
    if err:
        return err

    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return jsonify({
            "error": "ValidationError",
            "message": "skip and limit must be integers"
        }), 422

    skip = max(0, skip)
    limit = max(1, min(limit, 100))

    rows = list_for_user(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(rows),
        "items": history_list_schema.dump(rows),
    }), 200



@history_bp.get("/history/<int:song_id>")
def get_history(song_id: int):
    user_id, err = _require_user_id()
    if err:
        return err

    row = get_one_for_user(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    if row is None:
        return jsonify({
            "error": "NotFound",
            "message": "Song not found in history"
        }), 404

    return jsonify(history_read_schema.dump(row)), 200



@history_bp.delete("/history")
def clear_history():
    user_id, err = _require_user_id()
    if err:
        return err

    deleted = delete_all_for_user(
        db.session,
        user_id=user_id,
    )

    return jsonify({
        "status": "cleared",
        "deleted": deleted
    }), 200



@history_bp.delete("/history/<int:song_id>")
def delete_history(song_id: int):
    user_id, err = _require_user_id()
    if err:
        return err

    ok = delete_one_for_user(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    if not ok:
        return jsonify({
            "error": "NotFound",
            "message": "Song not found in history"
        }), 404

    return jsonify({
        "status": "deleted",
        "song_id": song_id
    }), 200
