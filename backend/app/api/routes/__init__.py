from flask import Flask

from app.api.routes.health import health_bp
from app.api.routes.songs import songs_bp
from app.api.routes.upload import uploads_bp
from app.api.routes.history import history_bp
from app.api.routes.users import users_bp
from app.api.routes.auth import auth_bp
from app.api.routes.analyze import analyze_bp


def register_routes(app: Flask) -> None:
    prefix = "/api/"

    app.register_blueprint(health_bp, url_prefix=prefix)
    app.register_blueprint(songs_bp, url_prefix=prefix)
    app.register_blueprint(uploads_bp, url_prefix=prefix)
    app.register_blueprint(history_bp, url_prefix=prefix)
    app.register_blueprint(users_bp, url_prefix=prefix)
    app.register_blueprint(auth_bp, url_prefix=prefix)
    app.register_blueprint(analyze_bp, url_prefix=prefix)


