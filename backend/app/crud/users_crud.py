# app/crud/users_crud.py
from __future__ import annotations

from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import User

def get_user_by_id(session: Session, *, user_id: int) -> Optional[User]:
    """
    Récupération d'un utilisateur par son identifiant.
    
    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur à récupérer
    - retourne :
        - l'objet User correspondant à l'identifiant si trouvé
        - None si aucun utilisateur n'existe avec cet identifiant
    """
    return session.get(User, user_id)

def get_user_by_email(session: Session, *, email: str) -> Optional[User]:
    """
    Récupération d'un utilisateur par son adresse e-mail.

    - session : instance SQLAlchemy Session
    - email : adresse e-mail de l'utilisateur à rechercher
    - retourne :
        - l'objet User correspondant à l'e-mail si trouvé
        - None si aucun utilisateur n'existe avec cette adresse e-mail
    """
    return session.query(User).filter(User.email == email).first()

def create_user_row(
    session: Session,
    *,
    name: str,
    email: str,
    password: str,
) -> User:
    """
    Création d'un nouvel utilisateur dans la base de données.

    - session : instance SQLAlchemy Session
    - name : nom de l'utilisateur
    - email : adresse e-mail de l'utilisateur
    - password : mot de passe
    - retourne :
        - l'objet User créé
    """
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

def list_users_basic(
    session: Session,
    *,
    limit: int = 50,
) -> List[User]:
    """
    Récupération d'une liste d'utilisateurs basique depuis la base de données.

    - session : instance SQLAlchemy Session
    - limit : nombre maximum d'utilisateurs à retourner
    - retourne :
        - une liste d'objets User limitée par limit
    """
    # Récupère limit s'il est entre 1 et 200 (1 ou 200 sinon)
    limit = max(1, min(int(limit), 200))

    # Retourne la liste des utilisateurs limitée par limit
    return (
        session.query(User)
        .order_by(User.user_id.desc())
        .limit(limit)
        .all()
    )

def get_user_by_email(db: Session, *, email: str) -> User | None:
    """
    Récupération d'un utilisateur par son adresse e-mail.

    - session : instance SQLAlchemy Session
    - email : adresse e-mail de l'utilisateur à rechercher
    - retourne :
        - l'objet User correspondant à l'e-mail si trouvé
        - None si aucun utilisateur n'existe avec cette adresse e-mail
    """
    return db.query(User).filter(User.email == email).first()

def authenticate_user(session: Session, *, email: str, password: str) -> Optional[User]:
    """
    Authentification d'un utilisateur via son email et son mot de passe.

    - session : instance SQLAlchemy Session
    - email : email de l'utilisateur
    - password : mot de passe
    - retourne :
        - l'objet User si l'authentification est réussie
        - None si l'email est invalide, le mot de passe est incorrect, ou l'utilisateur n'existe pas
    """
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

def user_public_dict(user: User) -> Dict[str, Any]:
    """
    Récupération d'une représentation publique d'un utilisateur

    - user : instance User
    - retourne :
        - dict contenant uniquement les champs publics : user_id, name, email
    """
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
    }
