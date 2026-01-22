from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db
from app.models.uploaded_by import UploadedBy
from app.schemas.uploaded_by_schema import UploadCreateSchema, UploadReadSchema, UploadUpdateSchema
from app.api.deps import get_request_user_id
from app.models.history import History
from app.models.song import Song

uploads_bp = Blueprint("uploads", __name__)

upload_create_schema = UploadCreateSchema()
upload_read_schema = UploadReadSchema()
upload_update_schema = UploadUpdateSchema()

@uploads_bp.post("/uploads")
def create_upload():
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    try:
        data = upload_create_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    upload = UploadedBy(
        song_id=data["song_id"],
        user_id=user_id,
        private=data["private"],
    )

    try:
        db.session.add(upload)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "IntegrityError",
            "message": "Upload cannot be created (FK missing or upload already exists for this song)."
        }), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "DatabaseError", "message": "Failed to create upload"}), 500

    return jsonify(upload_read_schema.dump(upload)), 201

@uploads_bp.patch("/uploads/<int:song_id>")
def patch_upload(song_id: int):
    # 1) "auth" dev: user_id obligatoire
    user_id = get_request_user_id()
    if user_id is None:
        return jsonify({"error": "Unauthorized", "message": "Missing X-User-Id (dev auth)"}), 401

    # 2) récupérer payload
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    # 3) valider
    try:
        data = upload_update_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    if "private" not in data:
        return jsonify({"error": "ValidationError", "message": "Provide 'private' (true/false)."}), 422

    # 4) récupérer upload
    upload = (
        db.session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )
    if upload is None:
        return jsonify({"error": "NotFound", "message": f"No upload found for song_id={song_id}"}), 404

    # 5) autorisation: seul l'uploader peut modifier
    if upload.user_id != user_id:
        return jsonify({"error": "Forbidden", "message": "Only the uploader can update this upload"}), 403

    # 6) update + commit
    upload.private = data["private"]

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "DatabaseError", "message": "Failed to update upload"}), 500

    return jsonify(upload_read_schema.dump(upload)), 200

@uploads_bp.get("/uploads/<int:song_id>")
def get_upload(song_id: int):
    upload = (
        db.session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )

    if upload is None:
        return jsonify({"error": "NotFound", "message": f"No upload found for song_id={song_id}"}), 404

    # ---- sécurité private ----
    if upload.private:
        user_id = get_request_user_id()
        if user_id is None:
            return jsonify({"error": "Forbidden", "message": "Private upload"}), 403
        if upload.user_id != user_id:
            return jsonify({"error": "Forbidden", "message": "Private upload"}), 403
    # -------------------------

    return jsonify(upload_read_schema.dump(upload)), 200
