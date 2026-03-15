#!/usr/bin/env python3
"""Email validation utilities."""

import re

# Simplified email regex pattern (not full RFC 5322; covers common valid formats)
_EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise.

    Validation rules:
    - Must be a non-empty string.
    - Must contain exactly one '@' character.
    - Local part (before '@') may contain letters, digits, and: . _ % + -
    - Domain part (after '@') must contain at least one dot.
    - Top-level domain must be at least two characters long.
    """
    if not isinstance(email, str) or not email:
        return False
    return bool(_EMAIL_PATTERN.match(email))
