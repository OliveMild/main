import re

_EMAIL_REGEX = re.compile(
    # Local part: no leading/trailing dots, no consecutive dots
    r"^[a-zA-Z0-9_%+\-]+(?:\.[a-zA-Z0-9_%+\-]+)*"
    r"@"
    # Domain: each label starts/ends with alphanumeric (no leading/trailing hyphens),
    # no consecutive dots; at least one subdomain plus a TLD of 2+ alpha chars.
    r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


class InvalidEmailError(ValueError):
    """Raised when an email address is invalid."""


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise."""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email: str) -> str:
    """Return *email* unchanged if it is valid.

    Raises:
        InvalidEmailError: If *email* is not a valid email address.
    """
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
