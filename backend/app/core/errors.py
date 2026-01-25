# app/core/errors.py

class AppError(Exception):
    status_code = 500
    error = "InternalServerError"

    def __init__(self, message: str | None = None):
        super().__init__(message)
        self.message = message or self.error


class BadRequestError(AppError):
    status_code = 400
    error = "BadRequest"


class UnauthorizedError(AppError):
    status_code = 401
    error = "Unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    error = "Forbidden"


class NotFoundError(AppError):
    status_code = 404
    error = "NotFound"


class ConflictError(AppError):
    status_code = 409
    error = "Conflict"
