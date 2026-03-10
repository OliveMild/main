"""Email validation utilities."""

import re

# Local part: no leading/trailing/consecutive dots; allowed chars: alnum, ._%+-
# Domain: labels separated by dots; each label is alnum/hyphen, no leading/trailing hyphens
# TLD: at least two letters
_EMAIL_PATTERN = re.compile(
    r"^(?![.\-])"                       # local part must not start with . or -
    r"[a-zA-Z0-9_%+\-]"                 # first char: alnum or special (not dot)
    r"(?:[a-zA-Z0-9._%+\-]*"            # middle chars
    r"[a-zA-Z0-9_%+\-])?"              # last char of local: not a dot
    r"@"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)"  # domain labels
    r"+[a-zA-Z]{2,}$"                   # TLD
)


class InvalidEmailError(ValueError):
    """Raised when an email address is invalid."""


def is_valid_email(email: object) -> bool:
    """Return True if *email* is a valid email address, False otherwise."""
    if not isinstance(email, str):
        return False
    if ".." in email.split("@")[0]:   # reject consecutive dots in the local part
        return False
    return bool(_EMAIL_PATTERN.match(email))


def validate_email(email: object) -> str:
    """Return *email* if it is valid, otherwise raise :exc:`InvalidEmailError`.

    :raises InvalidEmailError: If *email* is not a valid email address.
    """
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    assert isinstance(email, str)
    return email
