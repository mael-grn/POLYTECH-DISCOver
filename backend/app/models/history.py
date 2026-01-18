# app/models/history.py
from __future__ import annotations

from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class History(Base):
    __tablename__ = "history"

    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("song.song_id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    # dans ton schéma: last_research + date
    last_research: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    date: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    song: Mapped["Song"] = relationship(back_populates="history_entries")
    user: Mapped["User"] = relationship(back_populates="history_entries")


from backend.app.models.song import Song  # noqa: E402
from backend.app.models.user import User  # noqa: E402
