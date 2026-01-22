from flask import Flask

from app.core.config import DevConfig
from app.extensions import db, ma

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    ma.init_app(app)

    from app.api.routes import register_routes
    register_routes(app)

    return app
