from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.errors import NotFoundError, ForbiddenError
from app.extensions import db


def register_error_handlers(app: Flask):


    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({
            "error": "IntegrityError",
            "message": "Contrainte d'intégrité violée (clé étrangère manquante ou doublon)."
        }), 409


    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        db.session.rollback()
        return jsonify({
            "error": "DatabaseError",
            "message": "Une erreur est survenue lors de l'accès à la base de données"
        }), 500


    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({
            "error": "NotFound",
            "message": e.message
        }), 404

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(e):
        return jsonify({
            "error": "Forbidden",
            "message": e.message
        }), 403
