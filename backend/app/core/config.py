import os
from pathlib import Path
from dotenv import load_dotenv

# Charger l'environnement
load_dotenv()
# Chemin de app
BASE_DIR = Path(__file__).resolve().parents[2]

# Configuration
class Config:
    # Désactivation du suivi des modifications d'objet
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Préservation de l'ordre d'insertion initial
    JSON_SORT_KEYS = False

# Configuration côté Développeur
class DevConfig(Config):
    # Récupération des variables d'environnement pour la base de données
    # Récupération de l'utilisateur
    DB_USER = os.getenv("MYSQL_USER", "mael")
    # Récupération du mot de passe
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "mon_mot_de_passe_fort")
    # Récupération de l'hôte
    DB_HOST = os.getenv("MYSQL_HOST", "localhost")
    # Récupération du port
    DB_PORT = os.getenv("MYSQL_PORT", "3307")
    # Récupération du nom de la base de données
    DB_NAME = os.getenv("MYSQL_DATABASE", "discover_db")
    # Récupération de la clé secrète
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
    # Récupération de l'algorithme de signature des clés
    JWT_ALG = "HS256"
    # Récupération de la durée de vie du token (en secondes)
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))
    # Récupération de la chaîne de connexion SQLAlchemy pour la base de données
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
