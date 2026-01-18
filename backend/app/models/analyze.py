# app/models/analyze.py
from __future__ import annotations

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class Analyze(Base):
    __tablename__ = "analyze"

    # PK = song_id (=> 1 seule ligne Analyze par Song)
    id_song: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("song.song_id", ondelete="CASCADE"),
        primary_key=True,
    )

    popularity_probability: Mapped[float] = mapped_column(Float, nullable=False)

    song: Mapped["Song"] = relationship(
        back_populates="analyze",
        uselist=False,
    )


from backend.app.models.song import Song  # noqa: E402
