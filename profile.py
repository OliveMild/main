#!/usr/bin/env python3
"""Profile creation with validation."""

import re


class ProfileValidationError(ValueError):
    """Raised when profile data fails validation."""
    pass


def validate_profile(data: dict) -> None:
    """Validate profile data, raising ProfileValidationError on failure.

    Args:
        data: Dictionary containing profile fields.

    Required fields: name, email, age, username
    """
    required_fields = ["name", "email", "age", "username"]
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ProfileValidationError(f"'{field}' is required")

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ProfileValidationError("'name' must be a non-empty string")
    name_stripped = name.strip()
    if len(name_stripped) > 100:
        raise ProfileValidationError("'name' must be 100 characters or fewer")
    if not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*)*", name_stripped):
        raise ProfileValidationError(
            "'name' must contain only letters, spaces, hyphens, or apostrophes"
        )

    email = data["email"]
    if not isinstance(email, str) or not email.strip():
        raise ProfileValidationError("'email' must be a non-empty string")
    email_pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(email_pattern, email.strip()):
        raise ProfileValidationError("'email' is not a valid email address")

    age = data["age"]
    if not isinstance(age, int) or isinstance(age, bool):
        raise ProfileValidationError("'age' must be an integer")
    if age < 0 or age > 150:
        raise ProfileValidationError("'age' must be between 0 and 150")

    username = data["username"]
    if not isinstance(username, str) or not username.strip():
        raise ProfileValidationError("'username' must be a non-empty string")
    username_stripped = username.strip()
    if len(username_stripped) < 3 or len(username_stripped) > 30:
        raise ProfileValidationError("'username' must be between 3 and 30 characters")
    if not re.fullmatch(r"[A-Za-z0-9_]+", username_stripped):
        raise ProfileValidationError(
            "'username' must contain only letters, digits, or underscores"
        )


def create_profile(data: dict) -> dict:
    """Create and return a profile after validating the provided data.

    Args:
        data: Dictionary with profile fields (name, email, age, username).

    Returns:
        A new dictionary representing the created profile.

    Raises:
        ProfileValidationError: If any field fails validation.
    """
    validate_profile(data)
    return {
        "name": data["name"].strip(),
        "email": data["email"].strip().lower(),
        "age": data["age"],
        "username": data["username"].strip(),
    }
