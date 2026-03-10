#!/usr/bin/env python3
"""Custom error handlers for improved error management."""


class AppError(Exception):
    """Base class for application errors."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        if self.code is not None:
            return f"[{self.code}] {self.message}"
        return self.message


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, code=404)


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message="Validation failed"):
        super().__init__(message, code=400)


class UnauthorizedError(AppError):
    """Raised when an action is not authorized."""

    def __init__(self, message="Unauthorized"):
        super().__init__(message, code=401)


def handle_error(error):
    """Return a formatted error response dict for the given error."""
    if isinstance(error, AppError):
        return {"error": error.message, "code": error.code}
    return {"error": str(error), "code": 500}


def safe_call(func, *args, **kwargs):
    """Call func with args/kwargs and return (result, None) on success or
    (None, error_response) on failure."""
    try:
        return func(*args, **kwargs), None
    except Exception as exc:
        return None, handle_error(exc)
