from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.song_schema import SongCreateSchema, SongReadSchema
from app.schemas.song_list_schema import SongListItemSchema
from flask import g
from app.core.guards import require_auth

from app.crud.songs_crud import (
    create_song_row,
    get_song_with_private_guard,
    list_songs_with_upload_guard_and_search,
    list_my_songs_with_search,
    delete_uploaded_song_for_owner,
)

# Création d'un module pour les routes dérivant de songs
songs_bp = Blueprint("songs", __name__)

# Initialisation des différents schémas (création, lecture, liste, notre liste)
song_create_schema = SongCreateSchema()
song_read_schema = SongReadSchema()
songs_list_schema = SongListItemSchema(many=True)
songs_me_schema = SongListItemSchema(many=True)

# Gestion de la route "/songs" via post (Créé une chanson)
@songs_bp.post("/songs")
def create_song():
    # Lecture du JSON de la requête
    payload = request.get_json(silent=True)
    # S'il n'y a pas de JSON valide, renvoie une erreur
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON", "message": "Invalid or missing JSON body"}), 400

    # Conversion du JSON en dictionnaire Python
    try:
        data = song_create_schema.load(payload)
    # Renvoie une erreur si ça ne fonctionne pas
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    # Création de la chanson
    song = create_song_row(db.session, data=data)

    # Renvoie la chanson
    return jsonify(song_read_schema.dump(song)), 201

# Gestion de la route "/songs/<int:song_it>" via get (Indique une chanson)
@songs_bp.get("/songs/<int:song_id>")
@require_auth
def get_song(song_id: int):
    # Récupère l'identifiant de l'utilisateur
    maybe_user_id =  g.user_id

    # Récupère la chanson
    song = get_song_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=maybe_user_id,
        should_touch_history=True,
    )

    # Retourne la chanson
    return jsonify(song_read_schema.dump(song)), 200

# Gestion de la route "/songs" via get (Indique les chansons d'une recherche)
@songs_bp.get("/songs")
@require_auth
def list_songs():
    # Récupération de l'identifiant d'utilisateur
    maybe_user_id = g.user_id

    try:
        # Récupération de skip via l'URL (0 sinon)
        skip = int(request.args.get("skip", 0))
        # Récupération de limit via l'URL (50 sinon)
        limit = int(request.args.get("limit", 50))
    # Renvoie une erreur s'il y a une erreur de valeur
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    # Récupère skip s'il est positif (0 sinon)
    skip = max(skip, 0)
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(limit, 100))

    # Contenu de la recherche de chanson
    search = (request.args.get("q", "") or "").strip()
    # Mode de recherche ("any" (par défaut) == un mot correspond, "all" == tous les mots correspondent)
    mode = (request.args.get("mode", "any") or "any").strip().lower()  # any | all

    # Vérifie que si la recherche existe, que son contenu ne soit pas trop long (> 120 caractères)
    if search and len(search) > 120:
        return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
    # Vérifie que le mode soit "any" ou "all" et renvoie une erreur sinon
    if mode not in ("any", "all"):
        return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422

    # Récupère la liste des chansons correspondant à la recherche
    items = list_songs_with_upload_guard_and_search(
        db.session,
        maybe_user_id=maybe_user_id,
        skip=skip,
        limit=limit,
        search=search,
        mode=mode,
    )

    # Retourne la liste des chansons
    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_list_schema.dump(items),
    }), 200

# Gestion de la route "/songs/me" (Indique la recherche de nos chansons)
@songs_bp.get("/songs/me")
@require_auth
def list_my_songs():
    # Récupère l'identifiant d'utilisateur
    user_id =g.user_id

    try:
        # Récupération de skip via l'URL (0 sinon)
        skip = int(request.args.get("skip", 0))
        # Récupération de limit via l'URL (50 sinon)
        limit = int(request.args.get("limit", 50))
    # Renvoie une erreur s'il y a une erreur de valeur
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    # Récupère skip s'il est positif (0 sinon)
    skip = max(skip, 0)
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(limit, 100))

    # Contenu de la recherche de chanson
    search = (request.args.get("q", "") or "").strip()
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    mode = (request.args.get("mode", "any") or "any").strip().lower()

    # Vérifie que si la recherche existe, que son contenu ne soit pas trop long (> 120 caractères)
    if search and len(search) > 120:
        return jsonify({"error": "ValidationError", "message": "q is too long (max 120)"}), 422
    # Vérifie que le mode soit "any" ou "all" et renvoie une erreur sinon
    if mode not in ("any", "all"):
        return jsonify({"error": "ValidationError", "message": "mode must be 'any' or 'all'"}), 422

    # Récupère la liste des chansons correspondant à la recherche
    items = list_my_songs_with_search(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
        search=search,
        mode=mode,
    )

    # Retourne la liste des chansons
    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(items),
        "items": songs_me_schema.dump(items),
    }), 200

# Gestion de la route "/songs/<int:song_it>" via delete (Supprime une chanson)
@songs_bp.delete("/songs/<int:song_id>")
@require_auth
def delete_song(song_id: int):
    # Récupération de l'identifiant d'utilisateur
    user_id = g.user_id

    # Supprime la chanson
    delete_uploaded_song_for_owner(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    # Retourne la validation de suppression
    return jsonify({"status": "deleted", "song_id": song_id}), 200
