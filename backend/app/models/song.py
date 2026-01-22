
from __future__ import annotations

from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base


class Song(Base):
    __tablename__ = "song"

    song_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    song_name: Mapped[str] = mapped_column(String(255), nullable=False)

    song_popularity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    song_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    acousticness: Mapped[float | None] = mapped_column(Float, nullable=True)
    danceability: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy: Mapped[float | None] = mapped_column(Float, nullable=True)
    instrumentalness: Mapped[float | None] = mapped_column(Float, nullable=True)
    key: Mapped[int | None] = mapped_column(Integer, nullable=True)
    liveness: Mapped[float | None] = mapped_column(Float, nullable=True)
    loudness: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_in_data_set: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    analyze: Mapped["Analyze | None"] = relationship(
        back_populates="song",
        uselist=False,
        cascade="all, delete-orphan",
    )

    upload: Mapped["UploadedBy | None"] = relationship(
        back_populates="song",
        uselist=False,
        cascade="all, delete-orphan",
    )

    history_entries: Mapped[list["History"]] = relationship(
        back_populates="song",
        cascade="all, delete-orphan",
    )


from .analyze import Analyze
from .uploaded_by import UploadedBy
from .history import History
