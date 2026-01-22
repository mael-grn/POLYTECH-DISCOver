from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.history import History

def touch_history(user_id: int, song_id: int) -> None:
    """
    Crée ou met à jour une ligne d'historique pour (user_id, song_id).
    - si existe : update last_research
    - sinon : create date + last_research
    """
    now = datetime.now(timezone.utc)

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
