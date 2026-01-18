from flask import Flask
from .core.config import settings
from .core.db import db
from app.extensions import db, ma

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

    from backend.app.api.routes.songs import tracks_bp
    from backend.app.api.routes.users import users_bp

    app.register_blueprint(tracks_bp, url_prefix="/api/tracks")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app
