from functools import wraps
from flask import request, jsonify, g
from app.core.jwt_auth import verify_access_token, COOKIE_NAME

def require_auth(fn):
    """
    Nécessarisation d'une authentification par cookie JWT.

    - fn : fonction Flask
    - retourne :
        - le résultat de la fonction si authentification réussie
        - JSON {"error": "Unauthorized"} et code 401 si cookie manquant ou invalide
    """

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

from functools import wraps
from flask import g

def optional_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.cookies.get(COOKIE_NAME)

        if not token:
            g.user_id = None
            return fn(*args, **kwargs)

        user_id = verify_access_token(token)
        if user_id is None:
            g.user_id = None
            return fn(*args, **kwargs)

        g.user_id = int(user_id)
        return fn(*args, **kwargs)

    return wrapper
