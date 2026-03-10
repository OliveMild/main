#!/usr/bin/env python3
"""Email validation module."""

import re

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


def validate_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise.

    Non-string values are treated as invalid and return False.
    """
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email))
