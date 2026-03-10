#!/usr/bin/env python3
"""Email validation module."""

import re

_EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$'
)


def is_valid_email(email):
    """Check whether an email address is valid.

    Args:
        email: The value to check.

    Returns:
        True if *email* is a non-empty string that matches a standard
        email format, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(_EMAIL_PATTERN.match(email))
