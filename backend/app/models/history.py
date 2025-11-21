from datetime import datetime
from ..core.db import db

class SearchHistory(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)

    # Qui a fait la recherche ?
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="history_entries")

    # Sur quel morceau ?
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=True)
    track = db.relationship("Track", back_populates="history_entries")

    # Type de recherche: "dataset" (morceau du CSV) ou "upload" (MP3 envoyé)
    search_type = db.Column(db.String(20), nullable=False)

    # Nom affiché pour l'historique (ex : nom du fichier ou titre saisi)
    display_name = db.Column(db.String(255), nullable=False)

    # Résultat de l'analyse sérialisé en JSON (texte brut)
    # (ex: {"prediction": 0.82, "reason": "...", ...})
    result_json = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
