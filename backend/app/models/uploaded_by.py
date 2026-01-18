from __future__ import annotations

from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class UploadedBy(Base):
    __tablename__ = "uploaded_by"
    __table_args__ = (
        # Important : garantit 0..1 uploader par song (comme ton diagramme)
        UniqueConstraint("song_id", name="uq_uploaded_by_song_id"),
    )

    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("song.song_id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    date: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, server_default=func.now())
    private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    song: Mapped["Song"] = relationship(back_populates="upload")
    user: Mapped["User"] = relationship(back_populates="uploads")


from backend.app.models.song import Song
from backend.app.models.user import User
