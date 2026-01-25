# app/core/errors.py

# Erreur d'applications
class AppError(Exception):
    # Statut d'erreur d'application
    status_code = 500
    # Nom erreur application
    error = "InternalServerError"
    # Initialisation message erreur d'application
    def __init__(self, message: str | None = None):
        # Initialisation de la classe mère
        super().__init__(message)
        # Récupération du message ou de l'erreur
        self.message = message or self.error

# Erreur de mauvaises requêtes
class BadRequestError(AppError):
    # Statut mauvaise requête
    status_code = 400
    # Message mauvaise requête
    error = "BadRequest"

# Erreur de non-autorisations
class UnauthorizedError(AppError):
    # Statut non-authorisation
    status_code = 401
    # Message non-authorisation
    error = "Unauthorized"

# Erreur d'interdictions
class ForbiddenError(AppError):
    # Statut interdiction
    status_code = 403
    # Message interdiction
    error = "Forbidden"

# Erreur introuvables
class NotFoundError(AppError):
    # Statut introuvable
    status_code = 404
    # Message introuvable
    error = "NotFound"

# Erreur conflits
class ConflictError(AppError):
    # Statut conflit
    status_code = 409
    # Message conflit
    error = "Conflict"
