
from __future__ import annotations

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base


class Analyze(Base):
    __tablename__ = "analyze"

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


from .song import Song
