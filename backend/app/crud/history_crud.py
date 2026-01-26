# app/crud/history_crud.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.history import History
from app.core.errors import NotFoundError, ForbiddenError


def get_one_for_user(session: Session, *, user_id: int, song_id: int) -> Optional[History]:
    """
    Récupération de l'entrée d'historique d'une chanson pour un utilisateur donné.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur
    - song_id : identifiant de la chanson
    - retourne :
        - un objet History si une entrée est trouvée
        - None si aucune entrée correspondante n'existe
    """
    return (
        session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .first()
    )


def list_for_user(
    session: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
) -> List[History]:
    """
    Récupération de la liste des entrées d'historique d'un utilisateur avec pagination.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur dont on récupère l'historique
    - skip : nombre d'éléments à ignorer pour la pagination
    - limit : nombre maximal d'éléments à retourner
    - retourne : liste d'objets History correspondant aux critères
    """
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


def create_or_touch(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    now: Optional[datetime] = None,
) -> History:
    """
    Création ou mise à jour de l'entrée d'historique d'une chanson pour un utilisateur.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur
    - song_id : identifiant de la chanson
    - now : datetime du moment
    - retourne : l'objet History correspondant à l'utilisateur et la chanson, créé ou mis à jour
    """
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


def delete_all_for_user(session: Session, *, user_id: int) -> int:
    """
    Suppression de toutes les entrées d'historique pour un utilisateur donné.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur dont on supprime l'historique
    - retourne : nombre d'entrées supprimées
    """
    # Supprime l'historique
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id)
        .delete(synchronize_session=False)
    )
    # Renvoie le nombre d'entrées supprimées
    return int(deleted or 0)


def delete_one_for_user(session: Session, *, user_id: int, song_id: int) -> bool:
    """
    Suppression de l'entrée d'historique d'une chanson pour un utilisateur donné.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur
    - song_id : identifiant de la chanson dont on supprime l'historique
    - retourne :
        - True si une entrée a été supprimée
        - False si aucune entrée n'existait pour cette chanson et cet utilisateur
    """
    # Supprime l'historique de la chanson par rapport à l'utilisateur
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .delete(synchronize_session=False)
    )
    # Renvoie la confirmation de suppression
    return bool(deleted and deleted > 0)
