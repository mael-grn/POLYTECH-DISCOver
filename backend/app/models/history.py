
from __future__ import annotations

from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

# Création table History
class History(db.Model):
    # Création nom de table
    __tablename__ = "history"

    # Création colonne song_id (identifiant de chanson)
    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("song.song_id", ondelete="CASCADE"), primary_key=True
    )
    # Création colonne user_id (identifiant d'utilisateur)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    # Création colonne last_research (dernière recherche)
    last_research: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    # Création colonne date (Date)
    date: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Création colonne song (Chanson)
    song: Mapped["Song"] = relationship(back_populates="history_entries")
    # Création colonne user (Utilisateur)
    user: Mapped["User"] = relationship(back_populates="history_entries")


from app.models.song import Song
from app.models.user import User
