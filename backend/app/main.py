from . import create_app
from .core.base import Base         # ✅ Base SQLAlchemy 2.0
from .core.config import settings
from .core.db import db
from sqlalchemy import create_engine

# Crée le moteur SQLAlchemy pur
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)

app = create_app()

with app.app_context():
    db.create_all()  # ne crée que les tables manquantes
    print("Tables créées ou existantes ✅")

if __name__ == "__main__":
    app.run(debug=True)
