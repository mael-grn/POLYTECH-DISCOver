from flask import Blueprint, jsonify, current_app
from app.extensions import db

# Création d'un module pour les routes dérivant de health
health_bp = Blueprint("health", __name__)

# Gestion de la route "/health" (Indique la vie de l'API)
@health_bp.get("/health")
def health():
    # Retourne que l'API est vivante
    return jsonify({"status": "ok",
                    "database_uri": current_app.config.get("SQLALCHEMY_DATABASE_URI")}), 200
