from flask import Flask

from app.core.config import DevConfig
from app.extensions import db, ma
from app.api.routes import register_routes
from app.errors import *

def register_db_hooks(app: Flask) -> None:
    @app.teardown_request
    def _db_session_teardown(exception=None):
        # Si une exception a eu lieu pendant la requête => rollback
        if exception is not None:
            db.session.rollback()
            db.session.remove()
            return

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        finally:
            db.session.remove()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    ma.init_app(app)
    register_db_hooks(app)
    register_error_handlers(app)
    register_routes(app)

    return app
