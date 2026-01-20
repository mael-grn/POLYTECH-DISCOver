
from __future__ import annotations

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import db


class Analyze(db.Model):
    __tablename__ = "analyze"

    id_song: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Songs.id", ondelete="CASCADE"),
        primary_key=True,
    )

    popularity_probability: Mapped[float] = mapped_column(Float, nullable=False)

    song: Mapped["Song"] = relationship(
        "Song",
        back_populates="analyze",
        uselist=False,
    )


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .song import Song
