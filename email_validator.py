#!/usr/bin/env python3
import re

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_%+\-]+(\.[a-zA-Z0-9_%+\-]+)*@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$'
)


def is_valid_email(email: str) -> bool:
    """Return True if email is a valid email address, False otherwise."""
    if not isinstance(email, str):
        return False
    if '..' in email:
        return False
    return bool(EMAIL_REGEX.match(email))
