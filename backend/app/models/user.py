from datetime import datetime
from ..core.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relation avec l'historique
    history_entries = db.relationship(
        "SearchHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
