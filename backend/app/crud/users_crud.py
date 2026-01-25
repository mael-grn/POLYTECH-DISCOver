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

def get_user_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(session: Session, *, email: str, password: str) -> Optional[User]:

    email = (email or "").strip().lower()
    if not email or not password:
        return None

    user = get_user_by_email(session, email=email)
    if not user:
        return None

    return user if user.check_password(password) else None


def user_public_dict(user: User) -> Dict[str, Any]:

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
    }
def update_user(
    session: Session,
    *,
    user: User,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
) -> User:
    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

    if password is not None:
        user.set_password(password)

    session.flush()
    return user
