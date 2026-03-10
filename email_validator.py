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
    """Return True if *email* is a valid email address, False otherwise.

    Returns False for None and non-string inputs rather than raising.
    Requires a TLD of at least 2 characters (e.g. .com, .co.uk).
    """
    if email is None:
        return False
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_REGEX.match(email))


def validate_email(email):
    """Return *email* if it is valid, otherwise raise InvalidEmailError.

    Raises InvalidEmailError (a subclass of ValueError) for any input that
    is not a valid email address string, including None and non-string values.
    """
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email
