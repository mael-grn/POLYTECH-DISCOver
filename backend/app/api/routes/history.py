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
from flask import g
from app.core.guards import require_auth

# Création d'un module pour les routes dérivant de history
history_bp = Blueprint("history", __name__)

# Schemas
history_create_schema = HistoryCreateSchema()
history_read_schema = HistoryReadSchema()
history_list_schema = HistoryReadSchema(many=True)

# Gestion de la route "/history" via post (Créé l'historique)
@history_bp.post("/history")
@require_auth
def create_history():
    # Récupération de l'identifiant d'utilisateur
    user_id = g.user_id

    # Lecture du JSON de la requête
    payload = request.get_json(silent=True)
    # S'il n'y a pas de JSON valide, renvoie une erreur
    if payload is None:
        return jsonify({
            "error": "InvalidJSON",
            "message": "Request body must be valid JSON"
        }), 400

    # Conversion du JSON en dictionnaire Python
    try:
        data = history_create_schema.load(payload)
    # Renvoie une erreur si ça ne fonctionne pas
    except ValidationError as e:
        return jsonify({
            "error": "ValidationError",
            "messages": e.messages
        }), 422

    # Création ou mise à jour de l'historique
    row = create_or_touch(
        db.session,
        user_id=user_id,
        song_id=data["song_id"],
    )

    # Renvoie l'historique
    return jsonify(history_read_schema.dump(row)), 201

# Gestion de la route "/history" via get (Indique l'historique)
@history_bp.get("/history")
@require_auth
def list_history():
    # Récupération de l'identifiant d'utilisateur
    user_id = g.user_id

    try:
        # Récupération de skip via l'URL (0 sinon)
        skip = int(request.args.get("skip", 0))
        # Récupération de limit via l'URL (20 sinon)
        limit = int(request.args.get("limit", 20))
    # Renvoie une erreur s'il y a une erreur de valeur
    except ValueError:
        return jsonify({
            "error": "ValidationError",
            "message": "skip and limit must be integers"
        }), 422

    # Récupère skip s'il est positif (0 sinon)
    skip = max(0, skip)
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(limit, 100))

    # Récupération de l'historique
    rows = list_for_user(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    # Retourne l'historique
    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(rows),
        "items": history_list_schema.dump(rows),
    }), 200

# Gestion de la route "/history" via get (Récupère l'historique d'une chanson)
@history_bp.get("/history/<int:song_id>")
@require_auth
def get_history(song_id: int):
    # Récupère l'identifiant d'utilisateur
    user_id = g.user_id

    # Récupération de l'historique d'une chanson
    row = get_one_for_user(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    # Si elle n'existe pas dans l'historique, renvoie une erreur
    if row is None:
        return jsonify({
            "error": "NotFound",
            "message": "Song not found in history"
        }), 404

    # Renvoie l'historique de la chanson
    return jsonify(history_read_schema.dump(row)), 200

# Gestion de la route "/history" via delete (Supprime l'historique)
@history_bp.delete("/history")
@require_auth
def clear_history():
    # Récupération de l'identifiant d'utilisateur
    user_id = g.user_id

    # Supprime l'historique
    deleted = delete_all_for_user(
        db.session,
        user_id=user_id,
    )

    # Renvoie le message que tout est bon
    return jsonify({
        "status": "cleared",
        "deleted": deleted
    }), 200

# Gestion de la route "/history" via delete (Supprime l'historique d'une chanson)
@history_bp.delete("/history/<int:song_id>")
@require_auth
def delete_history(song_id: int):
    # Récupère l'identifiant d'utilisateur
    user_id = g.user_id
    
    # Suppression de l'historique d'une chanson
    ok = delete_one_for_user(
        db.session,
        user_id=user_id,
        song_id=song_id,
    )

    # Si la chanson n'existe pas, retourne une erreur
    if not ok:
        return jsonify({
            "error": "NotFound",
            "message": "Song not found in history"
        }), 404

    # Retourne la validation de la suppression
    return jsonify({
        "status": "deleted",
        "song_id": song_id
    }), 200
