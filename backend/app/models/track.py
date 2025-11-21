from ..core.db import db

class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(100), unique=True, index=True)  # id du dataset si présent
    artist_name = db.Column(db.String(255), index=True)
    track_name = db.Column(db.String(255), index=True)

    popularity = db.Column(db.Integer)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    tempo = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)

    # relation avec l'historique (recherches sur ce morceau)
    history_entries = db.relationship("SearchHistory", back_populates="track")

    def to_dict(self):
        return {
            "id": self.id,
            "track_id": self.track_id,
            "artist_name": self.artist_name,
            "track_name": self.track_name,
            "popularity": self.popularity,
            "danceability": self.danceability,
            "energy": self.energy,
            "acousticness": self.acousticness,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "loudness": self.loudness,
            "tempo": self.tempo,
            "duration_ms": self.duration_ms,
        }
