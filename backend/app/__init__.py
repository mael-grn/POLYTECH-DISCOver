from flask import Flask
from .core.config import settings
from .core.db import db

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = settings.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    db.init_app(app)

    # Import des blueprints API
    from .api.tracks import tracks_bp
    from .api.users import users_bp

    app.register_blueprint(tracks_bp, url_prefix="/api/tracks")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app
