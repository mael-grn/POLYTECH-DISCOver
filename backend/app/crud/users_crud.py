# app/crud/users_crud.py
from __future__ import annotations

from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import User

# Récupère un utilisateur par son identifiant
def get_user_by_id(session: Session, *, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

# Récupère un utilisateur par son e-mail
def get_user_by_email(session: Session, *, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()

# Créé un utilisateur
def create_user_row(
    session: Session,
    *,
    name: str,
    email: str,
    password: str,
) -> User:
    # Créé un utilisateur grâce à son nom et son email
    user = User(
        name=name,
        email=email,
    )
    # Met un mot de passe à l'utilisateur
    user.set_password(password)
    # Ajoute l'utilisateur
    session.add(user)
    # Retourne l'utilisateur
    return user

# Liste les utilisateurs
def list_users_basic(
    session: Session,
    *,
    limit: int = 50,
) -> List[User]:
    # Récupère limit s'il est entre 1 et 200 (1 ou 200 sinon)
    limit = max(1, min(int(limit), 200))

    # Retourne la liste des utilisateurs limitée par limit
    return (
        session.query(User)
        .order_by(User.user_id.desc())
        .limit(limit)
        .all()
    )

# Récupère un utilisateur par son e-mail
def get_user_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

# Authentification d'un utilisateur
def authenticate_user(session: Session, *, email: str, password: str) -> Optional[User]:
    # Récupération de l'email
    email = (email or "").strip().lower()
    # S'il n'y a pas d'e-mail ou de mot de passe, arrêter la fonction
    if not email or not password:
        return None

    # Récupère l'utilisateur par son email
    user = get_user_by_email(session, email=email)
    # Si l'utilisateur n'existe pas, arrêter la fonction
    if not user:
        return None

    # Si l'utilisateur a son mot de passe valide, retourne l'utilisateur, sinon rien
    return user if user.check_password(password) else None

# Récupère un dictionnaire contenant l'identifiant, le nom et l'e-mail d'un utilisateur
def user_public_dict(user: User) -> Dict[str, Any]:

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
    }
