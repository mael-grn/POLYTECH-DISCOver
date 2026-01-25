from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import check_password_hash

from app.extensions import db
from app.crud.user_crud import get_user_by_email
from app.core.jwt_auth import create_access_token, verify_access_token, COOKIE_NAME

# Création d'un module pour les routes dérivant de auth
auth_bp = Blueprint("auth", __name__)

# Gestion de la route "/auth/login" (Authentification)
@auth_bp.post("/auth/login")
def login():
    # Récupération des différentes données
    data = request.get_json(silent=True) or {}

    # Récupération de l'email
    email = (data.get("email") or "").strip().lower()
    # Récupération du mot de passe
    password = data.get("password") or ""

    # S'il n'y a pas d'email ou de mot de passe, renvoie une erreur
    if not email or not password:
        return jsonify({
            "error": "BadRequest",
            "message": "email and password required"
        }), 400

    # Authentification de l'utilisateur
    user = get_user_by_email(db.session, email=email)
    # Si l'utilisateur n'existe pas, renvoie une erreur
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # Si le mot de passe n'est pas le bon, renvoie une erreur
    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Unauthorized"}), 401

    # Génération de token
    token = create_access_token(user_id=user.id)

    # Création de la réponse HTTP
    resp = make_response(jsonify({"ok": True}), 200)
    # Configuration du cookie
    resp.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=int(current_app.config["JWT_EXP_SECONDS"]),
        path="/",
    )
    # Retourne la réponse
    return resp

# Gestion de la route "/auth/logout" (Déconnexion)
@auth_bp.post("/auth/logout")
def logout():
    # Création de la réponse HTTP
    resp = make_response(jsonify({"ok": True}), 200)
    # Suppression du cookie
    resp.delete_cookie(COOKIE_NAME, path="/")
    # Retourne la réponse
    return resp

# Gestion de la route "/auth/me" (Notre profil)
@auth_bp.get("/auth/me")
def me():
    # Récupération du cookie
    token = request.cookies.get(COOKIE_NAME)
    # S'il n'y a pas de cookie, cela indique la non-connexion
    if not token:
        return jsonify({"logged_in": False}), 200

    # Récupère l'identifiant d'utilisateur
    user_id = verify_access_token(token)
    # S'il n'y a pas d'identifiant d'utilisateur, cela indique la non-connexion
    if user_id is None:
        return jsonify({"logged_in": False}), 200

    # Retourne nos informations
    return jsonify({
        "logged_in": True,
        "user_id": user_id
    }), 200
