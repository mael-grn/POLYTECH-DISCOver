
from __future__ import annotations

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

# Création table analyse
class Analyze(db.Model):
    # Création nom de table
    __tablename__ = "analyze"

    # Création colonne id_song (identifiant de la chanson)
    id_song: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("song.song_id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Création colonne popularity_probability (score de popularité)
    popularity_probability: Mapped[float] = mapped_column(Float, nullable=False)

    # Création colonne song (chanson)
    song: Mapped["Song"] = relationship(
        back_populates="analyze",
        uselist=False,
    )


from app.models.song import Song
