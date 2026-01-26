from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.history import History
from app.api.deps import *

def touch_history(user_id: int, song_id: int) -> None:
    """
    Création ou mise à jour d'une entrée d'historique pour un utilisateur et une chanson donnés.

    - user_id : identifiant de l'utilisateur
    - song_id : identifiant de la chanson
    """
    now = datetime.now(timezone.utc)
    # Requête de l'historique en fonction de l'utilisateur et de la chanson
    row = (
        db.session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .first()
    )
    if row is None:
        row = History(user_id=user_id, song_id=song_id, date=now, last_research=now)
        db.session.add(row)
    else:
        row.last_research = now
def _require_user_id():
    """
    Récupération de l'identifiant utilisateur à partir des headers ou des paramètres de requête.

    - retourne :
        - le premier élément est l'identifiant utilisateur (int) si trouvé
        - le second élément est une réponse HTTP (Flask Response) d'erreur 401 si l'identifiant est manquant
        - None sinon
    """
    user_id = get_request_user_id()
    if user_id is None:
        return None, (
            jsonify({
                "error": "Unauthorized",
                "message": "Missing X-User-Id"
            }),
            401,
        )
    return user_id, None