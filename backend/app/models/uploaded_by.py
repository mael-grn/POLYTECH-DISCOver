from __future__ import annotations

from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

# Création table UploadedBy
class UploadedBy(db.Model):
    # Création nom de table
    __tablename__ = "uploaded_by"
    # Création contrainte d'unicité (song_id)
    __table_args__ = (
        UniqueConstraint("song_id", name="uq_uploaded_by_song_id"),
    )

    # Création colonne song_id (identifiant chanson)
    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("song.song_id", ondelete="CASCADE"), primary_key=True
    )
    # Création colonne user_id (identifiant utilisateur)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    # Création colonne date (Date)
    date: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, server_default=func.now())
    # Création colonne private (Privacité)
    private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Création colonne song (Chanson)
    song: Mapped["Song"] = relationship(back_populates="upload")
    # Création colonne user (Utilisateur)
    user: Mapped["User"] = relationship(back_populates="uploads")


from app.models.song import Song
from app.models.user import User
