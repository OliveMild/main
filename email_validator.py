#!/usr/bin/env python3
"""Email validation utilities."""

import re

_LOCAL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+$")
_LABEL_RE = re.compile(r"^[a-zA-Z0-9\-]+$")
_TLD_RE = re.compile(r"^[a-zA-Z]{2,}$")


class InvalidEmailError(ValueError):
    """Raised when an email address is not valid."""

    def __init__(self, email):
        super().__init__(f"Invalid email address: {email!r}")
        self.email = email


def is_valid_email(email):
    """Return True if *email* is a valid email address, False otherwise."""
    if not isinstance(email, str) or email.count("@") != 1:
        return False

    local, domain = email.split("@")

    # Validate local part: non-empty, no leading/trailing/consecutive dots.
    if not local or local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    if not _LOCAL_RE.match(local):
        return False

    # Validate domain: split into labels separated by dots.
    if not domain or domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    labels = domain.split(".")
    if len(labels) < 2:
        return False
    for label in labels:
        if not label or label.startswith("-") or label.endswith("-"):
            return False
        if not _LABEL_RE.match(label):
            return False

    # TLD must be letters only.
    if not _TLD_RE.match(labels[-1]):
        return False

    return True


def validate_email(email):
    """Return *email* if it is valid, otherwise raise InvalidEmailError."""
    if not is_valid_email(email):
        raise InvalidEmailError(email)
    return email
