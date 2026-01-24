
from __future__ import annotations

from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Song(db.Model):
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
    tempo: Mapped[float | None] = mapped_column(Float, nullable=True)
    audio_mode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    speechiness: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_signature: Mapped[int | None] = mapped_column(Integer, nullable=True)
    audio_valence: Mapped[float | None] = mapped_column(Float, nullable=True)
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

    def to_features_dict(self) -> Dict[str, Any]:
        return {
            "song_duration_ms": self.song_duration_ms,
            "tempo": self.tempo,
            "loudness": self.loudness,
            "key": self.key,
            "audio_mode": self.audio_mode,
            "time_signature": self.time_signature,
        }


from app.models.analyze import Analyze
from app.models.uploaded_by import UploadedBy
from app.models.history import History
