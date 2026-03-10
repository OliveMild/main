"""User profile module with data management and error handling."""

from __future__ import annotations

import re

_profiles: dict[int, dict] = {}
_next_id: int = 1

_EMAIL_RE = re.compile(r"^[^@\s]+@(?:[^@\s.]+\.)+[^@\s.]+$")


class UserProfileError(Exception):
    """Base class for user profile errors."""


class UserNotFoundError(UserProfileError):
    """Raised when a requested user profile does not exist."""

    def __init__(self, user_id: int) -> None:
        super().__init__(f"User with id {user_id} not found")
        self.user_id = user_id


class InvalidProfileDataError(UserProfileError):
    """Raised when profile data fails validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


def _validate(data: dict) -> None:
    """Validate profile fields; raise InvalidProfileDataError on failure."""
    name = data.get("name", "").strip()
    if not name:
        raise InvalidProfileDataError("'name' is required and cannot be blank")

    email = data.get("email", "").strip()
    if not email:
        raise InvalidProfileDataError("'email' is required and cannot be blank")
    if not _EMAIL_RE.match(email):
        raise InvalidProfileDataError(f"'{email}' is not a valid email address")


def create_profile(name: str, email: str) -> dict:
    """Create a new user profile and return it."""
    global _next_id
    _validate({"name": name, "email": email})
    profile = {"id": _next_id, "name": name.strip(), "email": email.strip()}
    _profiles[_next_id] = profile
    _next_id += 1
    return profile


def get_profile(user_id: int) -> dict:
    """Return the profile for *user_id* or raise UserNotFoundError."""
    if user_id not in _profiles:
        raise UserNotFoundError(user_id)
    return _profiles[user_id]


def update_profile(user_id: int, name: str, email: str) -> dict:
    """Update an existing profile and return the updated data."""
    if user_id not in _profiles:
        raise UserNotFoundError(user_id)
    _validate({"name": name, "email": email})
    _profiles[user_id].update({"name": name.strip(), "email": email.strip()})
    return _profiles[user_id]


def delete_profile(user_id: int) -> None:
    """Delete a profile or raise UserNotFoundError if it does not exist."""
    if user_id not in _profiles:
        raise UserNotFoundError(user_id)
    del _profiles[user_id]


def list_profiles() -> list[dict]:
    """Return all stored profiles."""
    return list(_profiles.values())


def _reset() -> None:
    """Reset module state (for testing)."""
    global _next_id
    _profiles.clear()
    _next_id = 1
