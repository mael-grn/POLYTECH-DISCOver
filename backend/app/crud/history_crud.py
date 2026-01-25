# app/crud/history_crud.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.history import History
from app.core.errors import NotFoundError, ForbiddenError

# Récupère l'historique d'une chanson par rapport à un utilisateur
def get_one_for_user(session: Session, *, user_id: int, song_id: int) -> Optional[History]:
    return (
        session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .first()
    )

# Récupère la liste d'historique d'un utilisateur
def list_for_user(
    session: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
) -> List[History]:
    # Récupère skip s'il est positif (0 sinon)
    skip = max(0, int(skip))
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(int(limit), 100))

    # Renvoie la liste d'historique d'un utilisateur
    return (
        session.query(History)
        .filter(History.user_id == user_id)
        .order_by(History.last_research.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

# Création ou Mise à jour d'un historique
def create_or_touch(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    now: Optional[datetime] = None,
) -> History:
    # S'il n'y a pas de date insérée, en créer une (la date du moment)
    if now is None:
        now = datetime.now(timezone.utc)

    # Récupère l'historique d'une chanson par rapport à un utilisateur
    row = get_one_for_user(session, user_id=user_id, song_id=song_id)

    # S'il n'y a pas d'historique
    if row is None:
        # Créer un historique
        row = History(
            user_id=user_id,
            song_id=song_id,
            date=now,
            last_research=now,
        )
        # Ajouter l'historique
        session.add(row)
    # Sinon, ajouter la date à l'historique
    else:
        row.last_research = now

    # Retourne l'historique
    return row

# Supprimer l'historique d'un utilisateur
def delete_all_for_user(session: Session, *, user_id: int) -> int:
    # Supprime l'historique
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id)
        .delete(synchronize_session=False)
    )
    # Renvoie la confirmation de suppression
    return int(deleted or 0)

# Supprimer l'historique d'une chanson par rapport à un utilisateur
def delete_one_for_user(session: Session, *, user_id: int, song_id: int) -> bool:
    # Supprime l'historique de la chanson par rapport à l'utilisateur
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .delete(synchronize_session=False)
    )
    # Renvoie la confirmation de suppression
    return bool(deleted and deleted > 0)
