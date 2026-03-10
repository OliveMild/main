#!/usr/bin/env python3
"""Email validation module providing robust email address validation."""

import re


class EmailValidationError(ValueError):
    """Raised when an email address fails validation."""


def validate_email(email: str) -> str:
    """Validate an email address and return the normalized lowercase form.

    Rules enforced:
    - Must be a string.
    - Must contain exactly one ``@`` character.
    - The local part (before ``@``) must be non-empty and contain no whitespace.
    - The domain part (after ``@``) must be non-empty, contain at least one
      dot, have no consecutive dots, and start/end without a dot or hyphen.
    - Overall length must not exceed 254 characters (RFC 5321).

    Args:
        email: The email address to validate.

    Returns:
        The normalized (lowercased, stripped) email address.

    Raises:
        EmailValidationError: If the email address is invalid.
    """
    if not isinstance(email, str):
        raise EmailValidationError("Email must be a string.")

    email = email.strip()

    if len(email) > 254:
        raise EmailValidationError("Email address exceeds maximum length of 254 characters.")

    if email.count("@") != 1:
        raise EmailValidationError(
            "Email address must contain exactly one '@' character."
        )

    local, domain = email.split("@")

    if not local:
        raise EmailValidationError("Local part (before '@') must not be empty.")

    if re.search(r"\s", local):
        raise EmailValidationError("Local part must not contain whitespace.")

    if not domain:
        raise EmailValidationError("Domain part (after '@') must not be empty.")

    if re.search(r"\s", domain):
        raise EmailValidationError("Domain part must not contain whitespace.")

    if "." not in domain:
        raise EmailValidationError("Domain must contain at least one dot.")

    if ".." in domain:
        raise EmailValidationError("Domain must not contain consecutive dots.")

    if domain.startswith(".") or domain.endswith("."):
        raise EmailValidationError("Domain must not start or end with a dot.")

    for label in domain.split("."):
        if label.startswith("-") or label.endswith("-"):
            raise EmailValidationError(
                "Domain labels must not start or end with a hyphen."
            )

    return email.lower()
