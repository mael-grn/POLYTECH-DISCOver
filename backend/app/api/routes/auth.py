from flask import Blueprint, request, jsonify, make_response, current_app

from app.extensions import db
from app.crud.users_crud import (
    authenticate_user,
    get_user_by_id,
    user_public_dict,
)
from app.core.jwt_auth import create_access_token, verify_access_token, COOKIE_NAME
# Création d'un module pour les routes dérivant de auth
auth_bp = Blueprint("auth", __name__)

# Gestion de la route "/auth/login"
@auth_bp.post("/auth/login")
def login():
    """
        Authentification d'un utilisateur et création d'un token JWT.

        - méthode : POST
        - retourne :
            - 200 et JSON {"ok": True} si succès
            - 400 si email ou mot de passe manquant
            - 401 si échec de l'authentification
        """
    # Récupération des différentes données
    data = request.get_json(silent=True) or {}
    # Récupération de l'email
    email = (data.get("email") or "").strip().lower()
    # Récupération du mot de passe
    password = data.get("password") or ""
    # S'il n'y a pas d'email ou de mot de passe, renvoie une erreur
    if not email or not password:
        return jsonify({"error": "BadRequest", "message": "email and password required"}), 400
    # Authentification de l'utilisateur
    user = authenticate_user(db.session, email=email, password=password)
    # Si l'utilisateur n'existe pas, renvoie une erreur
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    # Génération de token
    token = create_access_token(user_id=user.user_id)
    # Création de la réponse HTTP
    resp = make_response(jsonify({"ok": True}), 200)
    # Configuration du cookie
    resp.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=False,       # mets True en prod HTTPS
        samesite="Lax",
        max_age=int(current_app.config["JWT_EXP_SECONDS"]),
        path="/",
    )
    # Retourne la réponse
    return resp

# Gestion de la route "/auth/logout" (Déconnexion)
@auth_bp.post("/auth/logout")
def logout():
    """
        Déconnexion d'un utilisateur en supprimant son cookie d'authentification.

        - méthode : POST
        - retourne : JSON {"ok": True} avec code HTTP 200
        """
    # Création de la réponse HTTP
    resp = make_response(jsonify({"ok": True}), 200)
    # Suppression du cookie
    resp.delete_cookie(COOKIE_NAME, path="/")
    # Retourne la réponse
    return resp

# Gestion de la route "/auth/me"
@auth_bp.get("/auth/me")
def me():
    """
       Récupération des informations de l'utilisateur connecté via le cookie JWT.

       - méthode : GET
       - retourne :
           - 200 avec JSON {"logged_in": False} si non connecté
           - 200 avec JSON {"logged_in": True, "user": user} si connecté
       """
    # Récupération du cookie
    token = request.cookies.get(COOKIE_NAME)
    # S'il n'y a pas de cookie, cela indique la non-connexion
    if not token:
        return jsonify({"logged_in": False}), 200
    # Récupère l'identifiant d'utilisateur
    user_id = verify_access_token(token)
    if user_id is None:
        return jsonify({"logged_in": False}), 200

    # On passe par le CRUD
    user = get_user_by_id(db.session, user_id=int(user_id))
    # S'il n'y a pas d'identifiant d'utilisateur, cela indique la non-connexion
    if not user:
        # Token valide mais user supprimé / incohérent
        return jsonify({"logged_in": False}), 200
    # Retourne nos informations
    return jsonify({
        "logged_in": True,
        "user": user_public_dict(user),
    }), 200
