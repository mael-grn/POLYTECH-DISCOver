from flask import Flask
from flask_cors import CORS
from .core.config import settings
from .core.db import db
from .extensions import ma
from .api.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = settings.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config.from_object(settings)

    # 🔹 Activer CORS pour Flutter Web
    CORS(app, resources={r"/*": {"origins": "*"}})
    # tu peux mettre origins="*" si tu veux autoriser tous les domaines en dev

    db.init_app(app)
    ma.init_app(app)

    # ⚡️ Tout passe par register_routes
    register_routes(app)

    return app
