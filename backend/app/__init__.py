from flask import Flask

from app.core.config import DevConfig
from app.extensions import db, ma
from flask_cors import CORS
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(DevConfig)

    db.init_app(app)
    ma.init_app(app)

    from app.api.routes import register_routes
    register_routes(app)

    return app
