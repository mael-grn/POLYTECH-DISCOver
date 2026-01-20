from __future__ import annotations

from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import db


class UploadedBy(db.Model):
    __tablename__ = "uploaded_by"
    __table_args__ = (
        # Important : garantit 0..1 uploader par song (comme ton diagramme)
        UniqueConstraint("song_id", name="uq_uploaded_by_song_id"),
    )

    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Songs.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    date: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, server_default=func.now())
    private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    song: Mapped["Song"] = relationship("Song", back_populates="upload")
    user: Mapped["User"] = relationship("User", back_populates="uploads")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .song import Song
    from .user import User
