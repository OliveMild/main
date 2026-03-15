#!/usr/bin/env python3
"""Email validation module."""

import re

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


class InvalidEmailError(ValueError):
    """Raised when an email address fails validation."""


def validate_email(email: str) -> str:
    """Validate an email address and return it if valid.

    Args:
        email: The email address string to validate.

    Returns:
        The validated email address (stripped of surrounding whitespace).

    Raises:
        InvalidEmailError: If the email address is empty or has an invalid format.
    """
    if not isinstance(email, str):
        raise InvalidEmailError(f"Email must be a string, got {type(email).__name__}")

    email = email.strip()

    if not email:
        raise InvalidEmailError("Email address must not be empty")

    if not EMAIL_PATTERN.match(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")

    return email


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise."""
    try:
        validate_email(email)
        return True
    except InvalidEmailError:
        return False
