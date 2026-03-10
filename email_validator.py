"""Email validation utilities."""

import re

_EMAIL_RE = re.compile(
    r"^(?:[a-zA-Z0-9]"                    # local part starts with alphanumeric
    r"(?:[a-zA-Z0-9+\-]*"                 # alphanumeric, plus, hyphens (no dot here)
    r"(?:\.[a-zA-Z0-9+\-]+)*"            # dot-separated segments (no consecutive dots)
    r")?)"                                 # local part ends with alphanumeric or single char
    r"@"
    r"(?:[a-zA-Z0-9]"                     # domain label starts with alphanumeric
    r"(?:[a-zA-Z0-9\-]*"                  # domain label body
    r"[a-zA-Z0-9])?"                      # domain label ends with alphanumeric
    r"\.)"                                 # label separator (at least one dot required)
    r"+[a-zA-Z]{2,}$"                     # TLD: at least 2 alpha characters
)


class InvalidEmailError(ValueError):
    """Raised when an email address is not valid."""


def is_valid_email(email: object) -> bool:
    """Return True if *email* is a valid email address string, False otherwise.

    This function never raises; non-string inputs and ``None`` return ``False``.
    """
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_RE.match(email))


def validate_email(email: object) -> str:
    """Return *email* if it is valid, otherwise raise :class:`InvalidEmailError`.

    Args:
        email: The value to validate.

    Returns:
        The original email string when valid.

    Raises:
        InvalidEmailError: If *email* is not a string or does not match the
            expected email format.
    """
    if not is_valid_email(email):
        raise InvalidEmailError(f"Invalid email address: {email!r}")
    return email  # type: ignore[return-value]
