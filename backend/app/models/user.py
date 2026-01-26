from __future__ import annotations

from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Création table User
class User(db.Model):
    # Création nom de table
    __tablename__ = "user"
    # Création contrainte unicité (email)
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    # Création colonne user_id (identifiant utilisateur)
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Création colonne name (Nom)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # Création colonne email (E-mail)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    # Création colonne hashed_password (Mot de passe hashé)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Création colonne uploads (Téléversements)
    uploads: Mapped[list["UploadedBy"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Création colonne history_entries (Entrées dans l'historique)
    history_entries: Mapped[list["History"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str):
        """
        Hashage du mot de passe de l'utilisateur
        
        - self : table User
        - password : mot de passe à hacher
        """
        self.hashed_password  = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Vérification que le mot de passe est le bon
        
        - self : table Users
        - password : mot de passe à vérifier
        - retourne : booléen indiquant si le mot de passe est le bon
        """
        return check_password_hash(self.hashed_password , password)

from app.models.uploaded_by import UploadedBy
from app.models.history import History
