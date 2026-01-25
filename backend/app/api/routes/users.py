from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.api.deps import get_request_user_id
from app.extensions import db
from app.schemas.user_schema import UserCreateSchema

from app.crud.users_crud import (
    get_user_by_id,
    create_user_row,
    list_users_basic,
)
from flask import g
from app.core.guards import require_auth

# Création d'un module pour les routes dérivant de songs
users_bp = Blueprint("users", __name__)

# Initialisation du schéma de création
user_create_schema = UserCreateSchema()

# Gestion de la route "/users/me"
@users_bp.get("/users/me")
@require_auth
def get_me():
    """
    Récupération des informations de l'utilisateur connecté.

    - méthode : GET
    - retourne :
        - 200 et JSON contenant :
            - user_id : identifiant de l'utilisateur
            - name : nom de l'utilisateur
            - email : email de l'utilisateur
            - created_at : date de création du compte
        - 404 si l'utilisateur n'existe pas
    """
    # Récupère l'identifiant d'utilisateur
    user_id = g.user_id

    # Récupère l'utilisateur via son identifiant
    user = get_user_by_id(db.session, user_id=user_id)
    # Si l'utilisateur n'est pas présent, renvoie une erreur
    if user is None:
        return jsonify({"error": "NotFound", "message": f"User {user_id} not found"}), 404

    # Retourne l'utilisateur (nous-même)
    return jsonify({
        "user_id": user.user_id,
        "name": getattr(user, "name", None),
        "email": getattr(user, "email", None),
        "created_at": getattr(user, "created_at", None),
    }), 200

# Gestion de la route "/users"
@users_bp.post("/users")
def create_user():
    """
    Création d'un nouvel utilisateur.

    - méthode : POST
    - retourne :
        - 201 et JSON contenant :
            - user_id : identifiant de l'utilisateur créé
            - username : pseudo ou nom de l'utilisateur
            - name : nom complet de l'utilisateur
            - email : email de l'utilisateur
        - 400 si JSON manquant ou invalide
        - 422 si validation échoue
    """
    # Lecture du JSON de la requête
    payload = request.get_json(silent=True)
    # S'il n'y a pas de JSON valide, renvoie une erreur
    if payload is None:
        return jsonify({"error": "InvalidOrMissingJSON"}), 400

    # Conversion du JSON en dictionnaire Python
    try:
        data = user_create_schema.load(payload)
    # Renvoie une erreur si ça ne fonctionne pas
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    # Création de l'utilisateur
    user = create_user_row(
        db.session,
        name=data["name"],
        password=data["password"],
        email=data.get("email"),
    )

    # Renvoie l'utilisateur
    return jsonify({
        "user_id": user.user_id,
        "username": getattr(user, "username", getattr(user, "name", None)),
        "name": getattr(user, "name", None),
        "email": getattr(user, "email", None),
    }), 201

# Gestion de la route "/users"
@users_bp.get("/users")
def list_users():
    """
    Liste des utilisateurs existants

    - méthode : GET
    - retourne :
        - 200 et JSON contenant :
            - count : nombre d'utilisateurs retournés
            - items : liste des utilisateurs contenant :
                - user_id : identifiant de l'utilisateur
                - name : nom de l'utilisateur
                - email : email de l'utilisateur
    """
    # Récupération de limit via l'URL (50 sinon)
    limit = request.args.get("limit", 50, type=int)
    # Récupère limit s'il est entre 1 et 200 (1 ou 200 sinon)
    limit = max(1, min(limit, 200))

    # Récupère la liste des utilisateurs
    users = list_users_basic(db.session, limit=limit)

    # Renvoie la liste des utilisateurs
    return jsonify({
        "count": len(users),
        "items": [
            {
                "user_id": u.user_id,
                "name": getattr(u, "name", None),
                "email": getattr(u, "email", None),
            }
            for u in users
        ]
    }), 200
