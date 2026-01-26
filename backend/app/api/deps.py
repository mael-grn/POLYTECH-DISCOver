from flask import request
def get_request_user_id() -> int | None:
    """
    Récupère l'ID de l'utilisateur depuis l'en-tête HTTP X-User-Id.
    Utilisé pour l'authentification dev (mode développement).

    Retourne:
        - int : ID utilisateur si présent et valide
        - None : sinon (non authentifié)
    """
    raw = request.headers.get("X-User-Id") or request.args.get("user_id")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None