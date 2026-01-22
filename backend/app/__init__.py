from flask import Flask
from app.core.config import settings
from app.core.db import db
from app.extensions import ma
from app.api.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = settings.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config.from_object(settings)

    db.init_app(app)
    ma.init_app(app)
    register_routes(app)

    return app
