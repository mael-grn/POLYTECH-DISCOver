
from __future__ import annotations

from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

# Création table Song
class Song(db.Model):
    # Création nom de table
    __tablename__ = "song"

    # Création colonne song_id (identifiant de chanson)
    song_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Création colonne song_name (nom de chanson)
    song_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Création colonne song_popularity (popularité de chanson)
    song_popularity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Création colonne song_duration_ms (durée de chanson)
    song_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Création colonne acousticness (Acoustiquité)
    acousticness: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne danceability (Dançabilité)
    danceability: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne energy (Energie)
    energy: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne instrumentalness (Instrumentalité)
    instrumentalness: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne key (Tonalité)
    key: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Création colonne liveness (Vie)
    liveness: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne loudness (Bruyance)
    loudness: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne tempo (Tempo)
    tempo: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne audio_mode (Mode audio)
    audio_mode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Création colonne speechiness (Verbalité)
    speechiness: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne time_signature (Signature temporelle)
    time_signature: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Création colonne audio_valence (Valence audio)
    audio_valence: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Création colonne is_in_data_set (Existance dans l'ensemble de données)
    is_in_data_set: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Création colonne analyze (Analyse)
    analyze: Mapped["Analyze | None"] = relationship(
        back_populates="song",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Création colonne upload (Téléversement)
    upload: Mapped["UploadedBy | None"] = relationship(
        back_populates="song",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Création colonne history_entries (Entrées historiques)
    history_entries: Mapped[list["History"]] = relationship(
        back_populates="song",
        cascade="all, delete-orphan",
    )

    def to_features_dict(self) -> Dict[str, Any]:
        """
        Récupération des caractéristiques audio sous forme de dictionnaire
        
        - self : Table Song
        - retourne : dictionnaire de caractéristiques audios contenant :
            - "song_duration_ms" : Durée de la chanson en millisecondes
            - "tempo" : Tempo de la chanson
            - "loudness" : Bruyance de la chanson
            - "key" : Clé de la chanson
            - "audio_mode" : Mode audio de la chanson
            - "time_signature" : Signature temporelle de la chanson
        """
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
