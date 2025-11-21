import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Mode debug (log + reload)
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    # URL de connexion à MariaDB/MySQL
    # Exemple : mysql+pymysql://user:password@localhost:3306/song_popularity
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost:3306/song_popularity"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pour plus tard (auth JWT, etc.)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

settings = Settings()
