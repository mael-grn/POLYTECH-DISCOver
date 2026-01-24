# app/core/errors.py
from dataclasses import dataclass

@dataclass
class NotFoundError(Exception):
    message: str

@dataclass
class ForbiddenError(Exception):
    message: str
