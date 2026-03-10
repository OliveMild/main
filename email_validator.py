#!/usr/bin/env python3
"""Email validation module."""

import re

_EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_%+\-]+(\.[a-zA-Z0-9_%+\-]+)*'
    r'@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$'
)


def validate_email(email) -> bool:
    """Return True if *email* is a valid email address, False otherwise.

    Checks performed:
    - Must be a non-empty string
    - Total length must not exceed 320 characters
    - Must contain exactly one '@' character
    - Local and domain parts must be non-empty
    - No leading/trailing whitespace or embedded spaces
    - No consecutive dots in the local or domain part
    - Local part must not start or end with a dot
    - Domain must not start or end with a dot
    - Domain must have at least one dot with a TLD of 2+ characters
    """
    if not isinstance(email, str) or not email:
        return False

    if len(email) > 320:
        return False

    if ' ' in email:
        return False

    if email.count('@') != 1:
        return False

    local, domain = email.split('@')

    if not local or not domain:
        return False

    if '..' in local or '..' in domain:
        return False

    if local.startswith('.') or local.endswith('.'):
        return False

    if domain.startswith('.') or domain.endswith('.'):
        return False

    if not _EMAIL_REGEX.match(email):
        return False

    return True
