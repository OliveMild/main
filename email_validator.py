#!/usr/bin/env python3
"""Email validation module for user registration."""

import re


class InvalidEmailError(ValueError):
    """Raised when an email address fails validation."""


# RFC 5321 / RFC 5322 practical email regex.
# Allows standard local parts and domain labels separated by dots.
_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a syntactically valid email address.

    Args:
        email: The email address string to validate.

    Returns:
        True if the address is valid, False otherwise.
    """
    if not isinstance(email, str):
        return False
    if len(email) > 254:
        return False
    local, _, domain = email.rpartition("@")
    if not local or not domain:
        return False
    if len(local) > 64:
        return False
    return bool(_EMAIL_RE.match(email))


def validate_email(email: str) -> str:
    """Validate *email* and return it if valid, otherwise raise an error.

    Args:
        email: The email address string to validate.

    Returns:
        The original email string if valid.

    Raises:
        InvalidEmailError: if the email address is not valid.
    """
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
