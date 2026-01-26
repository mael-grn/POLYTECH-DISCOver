from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.errors import NotFoundError, ForbiddenError
from app.extensions import db
from app.core.errors import ConflictError

def register_error_handlers(app: Flask):
    """
    Enregistre des gestionnaires d'erreurs.

    - app : instance Flask
    - erreurs gérées :
        - IntegrityError (contrainte d'intégrité violée) -> 409
        - SQLAlchemyError (erreur base de données) -> 500
        - NotFoundError (ressource introuvable) -> 404
        - ForbiddenError (accès interdit) -> 403
        - ConflictError (conflit) -> 409
    - retourne : None
    """
    # Erreurs d'intégrité
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        # Retourne une erreur d'intégrité
        return jsonify({
            "error": "IntegrityError",
            "message": "Contrainte d'intégrité violée (clé étrangère manquante ou doublon)."
        }), 409

    # Erreur accès base de données
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        # Annule toutes les modifications non-enregistrées
        db.session.rollback()
        # Retourne une erreur de base de données
        return jsonify({
            "error": "DatabaseError",
            "message": "Une erreur est survenue lors de l'accès à la base de données"
        }), 500

    # Erreur "introuvable"
    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        # Retourne une erreur "non-trouvé"
        return jsonify({
            "error": "NotFound",
            "message": e.message
        }), 404

    # Erreur "interdit"
    @app.errorhandler(ForbiddenError)
    def handle_forbidden(e):
        # Retourne une erreur "interdite"
        return jsonify({
            "error": "Forbidden",
            "message": e.message
        }), 403

    # Erreur conflit
    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        # Retourne une erreur de conflit
        return jsonify({"error": "Conflict", "message": e.message}), 409
