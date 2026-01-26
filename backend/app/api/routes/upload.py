from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.uploaded_by_schema import (
    UploadCreateSchema,
    UploadReadSchema,
    UploadUpdateSchema,
)
import uuid
from app.core.guards import optional_auth
from pathlib import Path
from flask import g
from app.core.guards import require_auth
from app.services.audio_service import AudioAnalysisService
from app.services.ml_predictor import predict_popularity_score
from app.crud.uploads_crud import (
    create_upload_for_user,
    get_upload_by_song_id,
    get_upload_by_song_id_with_private_guard,
    set_upload_private_for_owner,
    list_my_uploads_with_song,
    create_upload_link
)
from app.crud.songs_crud import create_song_from_features
from app.crud.analyze_crud import upsert_analyze_for_song

uploads_bp = Blueprint("uploads", __name__)

upload_create_schema = UploadCreateSchema()
upload_read_schema = UploadReadSchema()
upload_update_schema = UploadUpdateSchema()
audio_service = AudioAnalysisService()
UPLOAD_DIR = Path("uploads_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXT = {".mp3"}




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

    upload, created = create_upload_for_user(
        db.session,
        user_id=user_id,
        song_id=data["song_id"],
        private=data["private"],
    )

    status = 201 if created else 200
    return jsonify(upload_read_schema.dump(upload)), status


@uploads_bp.patch("/uploads/<int:song_id>")
@require_auth
def patch_upload(song_id: int):
    # 1) "auth" dev: user_id obligatoire
    user_id = g.user_id
    # 2) récupérer payload
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400
    # 3) valider
    try:
        data = upload_update_schema.load(payload)
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "messages": e.messages}), 422

    if "private" not in data:
        return jsonify({"error": "ValidationError", "message": "Provide 'private' (true/false)."}), 422
    # 4) récupérer upload
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




@uploads_bp.post("/uploads/file")
@optional_auth
def upload_audio_file():
    user_id = g.user_id

    if "file" not in request.files:
        return jsonify({"error": "MissingFile", "message": "Provide multipart field 'file'."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "EmptyFilename"}), 400

    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "UnsupportedFileType", "message": "Only .mp3 is supported for now."}), 415

    private_raw = request.form.get("private", "true").lower().strip()
    private = private_raw in ("1", "true", "yes", "on")

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename
    f.save(filepath)

    analyzed_song = audio_service.analyze_file(str(filepath), str(f.filename).removesuffix(".mp3"))
    if analyzed_song is None:
        return jsonify({"error": "AudioAnalysisFailed"}), 500

    features = analyzed_song.to_features_dict()

    score = predict_popularity_score(features)

    song = create_song_from_features(db.session, song_name=analyzed_song.song_name, features=features, is_in_data_set=False)

    upsert_analyze_for_song(db.session, song_id=song.song_id, score_0_100=score)
    if user_id is not None:
        private_raw = request.form.get("private", "true").lower().strip()
        private = private_raw in ("1", "true", "yes", "on")
        create_upload_link(db.session, user_id=user_id, song_id=song.song_id, private=private)
    else:
        private = False

    return jsonify({
        "song_id": song.song_id,
        "song_name": song.song_name,
        "predicted_popularity": round(float(score), 1),
        "private": private,
        "stored_file": str(filepath),
    }), 201