import re

_EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_%+\-]+(?:\.[a-zA-Z0-9_%+\-]+)*'
    r'@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$'
)


class InvalidEmailError(ValueError):
    pass


def is_valid_email(email: str) -> bool:
    """Return True if email is a valid email address, False otherwise."""
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email: str) -> str:
    """Return email if valid, otherwise raise InvalidEmailError."""
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: '{email}'")
    return email
