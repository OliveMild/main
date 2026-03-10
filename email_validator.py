import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


class InvalidEmailError(ValueError):
    """Raised when an email address is invalid."""


def is_valid_email(email):
    """Return True if *email* is a valid email address, False otherwise."""
    if email is None:
        return False
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email):
    """Return *email* if it is valid, otherwise raise InvalidEmailError."""
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
