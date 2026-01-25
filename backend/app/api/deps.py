from flask import request

def get_request_user_id() -> int | None:
    """
    Récupèration de l'identifiant utilisateur depuis la requête HTTP.

    - retourne :
        - l'identifiant utilisateur entier si présent et valide
        - None si aucun identifiant n'est fourni ou si la conversion échoue
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
