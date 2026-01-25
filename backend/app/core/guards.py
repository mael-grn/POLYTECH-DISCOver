from functools import wraps
from flask import request, jsonify, g
from app.core.jwt_auth import verify_access_token, COOKIE_NAME

# Nécessarisation authentification
def require_auth(fn):
    # Création wrapper
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Récupération du cookie
        token = request.cookies.get(COOKIE_NAME)
        # S'il n'y a pas de cookie, renvoie une erreur
        if not token:
            return jsonify({"error": "Unauthorized"}), 401

        # Vérifie la validité du cookie (identifiant utilisateur)
        user_id = verify_access_token(token)
        # Si le cookie est invalide, renvoie une erreur
        if user_id is None:
            return jsonify({"error": "Unauthorized"}), 401

        # Stockage de l'identifiant utilisateur
        g.user_id = int(user_id)
        # Appelle la fonction originale
        return fn(*args, **kwargs)
    # Renvoie wrapper
    return wrapper
