#!/usr/bin/env python3
import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_%+\-]"           # local part: must start with non-dot
    r"(?:[a-zA-Z0-9_%+\-]*"        # local part: middle chars (no dot yet)
    r"(?:\.[a-zA-Z0-9_%+\-]+)*)"   # local part: single dots between groups
    r"?"                            # allow single-char local part
    r"@"
    r"(?:[a-zA-Z0-9]"              # domain: label starts with alnum
    r"(?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?"  # domain: optional middle + end
    r"\.)+"                         # domain: one or more labels followed by dot
    r"[a-zA-Z]{2,}$"               # TLD: two or more letters
)


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a valid e-mail address, False otherwise."""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email.strip()))
