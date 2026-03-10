#!/usr/bin/env python3
"""Email validation utilities."""

import re

EMAIL_MAX_LENGTH = 254

_LOCAL = r"[a-zA-Z0-9_%+\-]+(\.[a-zA-Z0-9_%+\-]+)*"
_LABEL = r"[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?"
_EMAIL_RE = re.compile(
    rf"^{_LOCAL}@({_LABEL}\.)+[a-zA-Z]{{2,}}$"
)


class InvalidEmailError(ValueError):
    """Raised when an email address fails validation."""


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a syntactically valid email address.

    Validation rules:
    - Must be a non-empty string
    - Length must not exceed EMAIL_MAX_LENGTH (254 characters per RFC 5321)
    - Must match the pattern: local@domain.tld
    """
    if not isinstance(email, str):
        return False
    if not email or len(email) > EMAIL_MAX_LENGTH:
        return False
    return bool(_EMAIL_RE.match(email))


def validate_email(email: str) -> str:
    """Validate *email* and return it, or raise InvalidEmailError.

    Args:
        email: The email address to validate.

    Returns:
        The validated email address (stripped of leading/trailing whitespace).

    Raises:
        InvalidEmailError: If the email address is not valid.
    """
    if isinstance(email, str):
        email = email.strip()
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
