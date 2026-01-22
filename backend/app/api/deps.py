# backend/app/api/deps.py
from typing import Optional
from flask import request

def get_request_user_id() -> Optional[int]:
    """
    Récupère l'ID de l'utilisateur depuis l'en-tête HTTP X-User-Id.
    Utilisé pour l'authentification dev (mode développement).

    Retourne:
        - int : ID utilisateur si présent et valide
        - None : sinon (non authentifié)
    """
    user_id = request.headers.get("X-User-Id")
    if user_id is None:
        return None
    try:
        return int(user_id)
    except ValueError:
        return None
