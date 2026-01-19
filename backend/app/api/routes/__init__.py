from flask import Flask

from app.routes.health import health_bp
from app.routes.songs import songs_bp

def register_routes(app: Flask) -> None:
    prefix = "/api/v1"

    app.register_blueprint(health_bp, url_prefix=prefix)
    app.register_blueprint(songs_bp, url_prefix=prefix)
