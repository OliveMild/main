#!/usr/bin/env python3
"""Email validation module."""

import re

_LABEL = r"[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?"
_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_%+-]+(\.[a-zA-Z0-9_%+-]+)*"
    r"@"
    rf"({_LABEL}\.)*{_LABEL}\.[a-zA-Z]{{2,}}$"
)


def is_valid_email(email: object) -> bool:
    """Return True if *email* is a valid email address, False otherwise.

    Rejects non-strings, empty strings, addresses missing the local part
    or domain, addresses with consecutive dots, multiple '@' characters,
    and domains without a TLD of at least two characters.
    """
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email:
        return False
    if ".." in email:
        return False
    return bool(_EMAIL_REGEX.match(email))
