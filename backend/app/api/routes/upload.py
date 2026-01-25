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

# Création d'un module pour les routes dérivant de uploads
uploads_bp = Blueprint("uploads", __name__)

# Initialisation des différents schémas (Création, Lecture, Mise à jour)
upload_create_schema = UploadCreateSchema()
upload_read_schema = UploadReadSchema()
upload_update_schema = UploadUpdateSchema()
# Service Audio
audio_service = AudioAnalysisService()
# Création du dossier d'uploads
UPLOAD_DIR = Path("uploads_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# MP3 uniquement autorisés
ALLOWED_EXT = {".mp3"}

# Gestion de la route "/uploads" (Créé un upload)
@uploads_bp.post("/uploads")
@require_auth
def create_upload():
    # Récupère l'identifiant de l'utilisateur
    user_id = g.user_id

    # Lecture du JSON de la requête
    payload = request.get_json(silent=True)
    # S'il n'y a pas de JSON valide, renvoie une erreur
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    # Conversion du JSON en dictionnaire Python
    try:
        data = upload_create_schema.load(payload)
    # Renvoie une erreur si ça ne fonctionne pas
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "messages": e.messages}), 422

    # Création de l'upload
    upload, created = create_upload_for_user(
        db.session,
        user_id=user_id,
        song_id=data["song_id"],
        private=data["private"],
    )
    
    # Si l'upload est nouveau, status reçoit 201, sinon 200
    status = 201 if created else 200
    # Retourne l'upload
    return jsonify(upload_read_schema.dump(upload)), status

# Gestion de la route "/uploads/<int:song_it>" via patch (Créé un upload privé ou public)
@uploads_bp.patch("/uploads/<int:song_id>")
@require_auth
def patch_upload(song_id: int):
    # Récupère l'identifiant de l'utilisateur
    user_id = g.user_id

    # Lecture du JSON de la requête
    payload = request.get_json(silent=True)
    # S'il n'y a pas de JSON valide, renvoie une erreur
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    # Conversion du JSON en dictionnaire Python
    try:
        data = upload_update_schema.load(payload)
    # Renvoie une erreur si ça ne fonctionne pas
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "messages": e.messages}), 422

    # Si le champ "private" n'existe pas, retourne une erreur
    if "private" not in data:
        return jsonify({"error": "ValidationError", "message": "Provide 'private' (true/false)."}), 422

    # Rend la chanson privée ou non par rapport à l'utilisateur
    upload = set_upload_private_for_owner(
        db.session,
        user_id=user_id,
        song_id=song_id,
        private=data["private"],
    )

    # Retourne l'upload
    return jsonify(upload_read_schema.dump(upload)), 200

# Gestion de la route "/uploads/<int:song_it>" via get (Indique un upload)
@uploads_bp.get("/uploads/<int:song_id>")
@require_auth
def get_upload(song_id: int):
    # Récupère l'identifiant de l'utilisateur
    user_id = g.user_id
    # Récupère l'upload
    upload = get_upload_by_song_id_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=user_id,
    )
    # Renvoie l'upload
    return jsonify(upload_read_schema.dump(upload)), 200

# Gestion de la route "/uploads/me" (Indique nos uploads)
@uploads_bp.get("/uploads/me")
@require_auth
def get_my_uploads():
    # Récupère l'identifiant d'utilisateur
    user_id = g.user_id

    # Récupération de skip via l'URL (0 sinon)
    skip = request.args.get("skip", 0, type=int)
    # Récupération de limit via l'URL (50 sinon)
    limit = request.args.get("limit", 50, type=int)
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(limit, 100))

    # Liste nos uploads avec les chansons associées
    items = list_my_uploads_with_song(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    # Retourne nos uploads
    return jsonify({
        "count": len(items),
        "items": items,
    }), 200

# Gestion de la route "/uploads/file" (Upload un fichier)
@uploads_bp.post("/uploads/file")
@require_auth
def upload_audio_file():
    # Récupère l'identifiant d'utilisateur
    user_id = g.user_id

    # Si le fichier n'existe pas, renvoie une erreur
    if "file" not in request.files:
        return jsonify({"error": "MissingFile", "message": "Provide multipart field 'file'."}), 400

    # Récupération du fichier
    f = request.files["file"]
    # Si le fichier n'a pas de nom, renvoie une erreur
    if not f.filename:
        return jsonify({"error": "EmptyFilename"}), 400

    # Création de l'extension
    ext = Path(f.filename).suffix.lower()
    # Si l'extension n'est pas supportée, renvoie une erreur
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "UnsupportedFileType", "message": "Only .mp3 is supported for now."}), 415

    # Vérification de la privacité
    private_raw = request.form.get("private", "true").lower().strip()
    # Conversion en booléen
    private = private_raw in ("1", "true", "yes", "on")

    # Génération d'un nom de fichier
    filename = f"{uuid.uuid4().hex}{ext}"
    # Chemin du fichier
    filepath = UPLOAD_DIR / filename
    # Enregistrement du fichier
    f.save(filepath)

    # Extraction des caractéristiques audio
    analyzed_song = audio_service.analyze_file(str(filepath))
    # Si l'extraction est vide, renvoie une erreur
    if analyzed_song is None:
        return jsonify({"error": "AudioAnalysisFailed"}), 500

    # Transformation des caractéristiques en dictionnaire
    features = analyzed_song.to_features_dict()
    # Création d'un score de popularité
    score = predict_popularity_score(features)
    # Création d'une nouvelle chanson dans la base de données
    song = create_song_from_features(db.session, song_name=analyzed_song.song_name, features=features, is_in_data_set=False)

    # Mise à jour de Analyze
    upsert_analyze_for_song(db.session, song_id=song.song_id, score_0_100=score)
    # Créé un lien d'upload privé ou public
    create_upload_link(db.session, user_id=user_id, song_id=song.song_id, private=private)

    # Retourne l'upload créé
    return jsonify({
        "song_id": song.song_id,
        "song_name": song.song_name,
        "predicted_popularity": round(float(score), 1),
        "private": private,
        "stored_file": str(filepath),
    }), 201