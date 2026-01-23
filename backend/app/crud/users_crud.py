# app/crud/users_crud.py
from __future__ import annotations

from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_id(session: Session, *, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_email(session: Session, *, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()


def create_user_row(
    session: Session,
    *,
    name: str,
    email: str,
    password: str,
) -> User:
    user = User(
        name=name,
        email=email,
    )

    user.set_password(password)

    session.add(user)
    return user


def list_users_basic(
    session: Session,
    *,
    limit: int = 50,
) -> List[User]:
    limit = max(1, min(int(limit), 200))

    return (
        session.query(User)
        .order_by(User.user_id.desc())
        .limit(limit)
        .all()
    )
