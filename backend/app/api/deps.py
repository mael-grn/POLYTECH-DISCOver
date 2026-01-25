from flask import request

# Fonction récupérant l'identifiant de l'utilisateur dans une requête
def get_request_user_id() -> int | None:
    """
    """
    # Récupération de l'identifiant de l'utilisateur
    raw = request.headers.get("X-User-Id") or request.args.get("user_id")
    # S'il n'y en a pas, retourne None
    if not raw:
        return None
    # Retourne l'identifiant sous forme entière
    try:
        return int(raw)
    # Si une erreur apparaît, retourne None
    except ValueError:
        return None
