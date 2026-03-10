import re

# Local part: starts with alphanumeric; allows dots separated by at least one
# non-dot character (consecutive dots are not permitted by the group structure).
# Domain: each label starts/ends with alphanumeric, no consecutive dots,
# TLD must be at least 2 characters.
_LOCAL = r"[a-zA-Z0-9][a-zA-Z0-9_+\-]*(?:\.[a-zA-Z0-9_+\-]+)*"
_LABEL = r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?"
_DOMAIN = rf"(?:{_LABEL}\.)+[a-zA-Z]{{2,}}"
_EMAIL_REGEX = re.compile(rf"^{_LOCAL}@{_DOMAIN}$")


class InvalidEmailError(ValueError):
    """Raised when an email address does not match the expected format."""


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a well-formed email address, False otherwise."""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email: str) -> str:
    """Return *email* unchanged if it is valid, otherwise raise InvalidEmailError."""
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
