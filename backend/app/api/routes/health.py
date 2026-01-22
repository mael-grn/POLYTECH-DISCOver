from flask import Blueprint, jsonify, current_app
from app.extensions import db


health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok",
                    "database_uri": current_app.config.get("SQLALCHEMY_DATABASE_URI")}), 200
