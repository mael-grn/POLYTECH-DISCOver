import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevConfig(Config):
    # Récupération des variables d'environnement pour la base de données

    DB_USER = os.getenv("MYSQL_USER", "mael")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "mon_mot_de_passe_fort")
    DB_HOST = os.getenv("MYSQL_HOST", "localhost")
    DB_PORT = os.getenv("MYSQL_PORT", "3307")
    DB_NAME = os.getenv("MYSQL_DATABASE", "discover_db")
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
    JWT_ALG = "HS256"
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
