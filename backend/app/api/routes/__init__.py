from flask import Flask

from .songs import songs_bp
from .users import users_bp
from .health import health_bp

def register_routes(app):
    app.register_blueprint(songs_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(health_bp)
