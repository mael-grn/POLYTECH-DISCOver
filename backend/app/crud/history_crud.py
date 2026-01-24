# app/crud/history_crud.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.history import History
from app.core.errors import NotFoundError, ForbiddenError


def get_one_for_user(session: Session, *, user_id: int, song_id: int) -> Optional[History]:
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
    skip = max(0, int(skip))
    limit = max(1, min(int(limit), 100))

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
    if now is None:
        now = datetime.now(timezone.utc)

    row = get_one_for_user(session, user_id=user_id, song_id=song_id)

    if row is None:
        row = History(
            user_id=user_id,
            song_id=song_id,
            date=now,
            last_research=now,
        )
        session.add(row)
    else:
        row.last_research = now

    return row


def delete_all_for_user(session: Session, *, user_id: int) -> int:
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id)
        .delete(synchronize_session=False)
    )
    return int(deleted or 0)


def delete_one_for_user(session: Session, *, user_id: int, song_id: int) -> bool:
    deleted = (
        session.query(History)
        .filter(History.user_id == user_id, History.song_id == song_id)
        .delete(synchronize_session=False)
    )
    return bool(deleted and deleted > 0)
