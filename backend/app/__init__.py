from flask import Flask

from app.core.config import DevConfig
from app.extensions import db, ma
from app.api.routes import register_routes
from app.errors import *

# Enregistrement de hooks pour chaque requête
def register_db_hooks(app: Flask) -> None:
    """
    Enregistre des hooks pour chaque requête

    - app : instance Flask
    - retourne : None
    """
    # Gestion des exceptions
    @app.teardown_request
    def _db_session_teardown(exception=None):
        # Si une exception a eu lieu pendant la requête => rollback
        if exception is not None:
            # Annule toutes les modifications non-enregistrées
            db.session.rollback()
            # Supprime la session
            db.session.remove()
            # Arrête la fonction
            return

        # Enregistre les modifications
        try:
            db.session.commit()
        # S'il y a une erreur, annuler les modifications et lever l'exception
        except SQLAlchemyError:
            db.session.rollback()
            raise

        finally:
            db.session.remove()

def create_app() -> Flask:
    """
    Crée et configure l'application Flask.

    - retourne : instance Flask configurée
    """
    app = Flask(__name__)
    # Chargement de la configuration
    app.config.from_object(DevConfig)

    # Initialisation de la base des modules nécessaires (marshmallow, db)
    db.init_app(app)
    ma.init_app(app)
    register_db_hooks(app)
    # Gestion des erreurs
    register_error_handlers(app)
    from app.api.routes import register_routes
    # Enregistrement des routes
    register_routes(app)

    return app
