import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


class InvalidEmailError(ValueError):
    def __init__(self, email):
        super().__init__(f"Invalid email address: {email!r}")


def is_valid_email(email):
    """Return True if email is a valid email address, False otherwise."""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email):
    """Return email if valid, otherwise raise InvalidEmailError."""
    if not is_valid_email(email):
        raise InvalidEmailError(email)
    return email
