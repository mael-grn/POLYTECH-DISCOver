import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevConfig(Config):
    # base SQLite dans backend/dev.bd
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"sqlite:///{(BASE_DIR / 'dev.bd').as_posix()}",
    )


