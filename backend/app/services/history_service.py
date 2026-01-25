from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.history import History
from app.api.deps import *

def touch_history(user_id: int, song_id: int) -> None:
    """
    Crée ou met à jour une ligne d'historique pour (user_id, song_id).
    - si existe : update last_research
    - sinon : create date + last_research
    """
    # Date du moment
    now = datetime.now(timezone.utc)

    # Requête de l'historique en fonction de l'utilisateur et de la chanson
    row = (
        db.session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .first()
    )
    # Si la requête est vide
    if row is None:
        # Crée un historique
        row = History(user_id=user_id, song_id=song_id, date=now, last_research=now)
        # Ajoute cet historique
        db.session.add(row)
    # Sinon, ajouter la date du moment à la recherche
    else:
        row.last_research = now

# Récupère l'identifiant utilisateur
def _require_user_id():
    # Récupère l'identifiant utilisateur
    user_id = get_request_user_id()
    # Si l'utilisateur est vide, retourne un message d'erreur
    if user_id is None:
        return None, (
            jsonify({
                "error": "Unauthorized",
                "message": "Missing X-User-Id"
            }),
            401,
        )
    # Retourne l'identifiant utilisateur
    return user_id, None
