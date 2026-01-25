from flask import Flask

from app.api.routes.health import health_bp
from app.api.routes.songs import songs_bp
from app.api.routes.upload import uploads_bp
from app.api.routes.history import history_bp
from app.api.routes.users import users_bp
from app.api.routes.dev import dev_bp
from app.api.routes.auth import auth_bp
from app.api.routes.analyze import analyze_bp

# Création des différentes routes
def register_routes(app: Flask) -> None:
    # Récupération du préfixe commun
    prefix = "/api/"

    # Route health
    app.register_blueprint(health_bp, url_prefix=prefix)
    # Route songs
    app.register_blueprint(songs_bp, url_prefix=prefix)
    # Route uploads
    app.register_blueprint(uploads_bp, url_prefix=prefix)
    # Route history
    app.register_blueprint(history_bp, url_prefix=prefix)
    # Route users
    app.register_blueprint(users_bp, url_prefix=prefix)
    # Route dev
    app.register_blueprint(dev_bp, url_prefix=prefix)
    # Route auth
    app.register_blueprint(auth_bp, url_prefix=prefix)
    # Route analyze
    app.register_blueprint(analyze_bp, url_prefix=prefix)


