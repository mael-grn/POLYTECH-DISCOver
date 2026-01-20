
from __future__ import annotations

from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import db


class History(db.Model):
    __tablename__ = "history"

    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Songs.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    last_research: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    date: Mapped["DateTime"] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    song: Mapped["Song"] = relationship("Song", back_populates="history_entries")
    user: Mapped["User"] = relationship("User", back_populates="history_entries")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .song import Song
    from .user import User
