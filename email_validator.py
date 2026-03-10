import re

_LOCAL_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_+\-]*(?:\.[a-zA-Z0-9_+\-]+)*$")
_LABEL_RE = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?$")
_TLD_RE = re.compile(r"^[a-zA-Z]{2,}$")


class EmailNotValidError(ValueError):
    """Raised when an email address does not match the expected format."""


# Backward-compatible alias
InvalidEmailError = EmailNotValidError


def _check_email(email: str) -> None:
    """Validate *email* and raise EmailNotValidError with a specific reason if invalid."""
    if not isinstance(email, str):
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The value is not a string."
        )

    at_count = email.count("@")

    if at_count == 0:
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The email address does not contain an @-sign."
        )

    if at_count > 1:
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The part after the @-sign contains invalid characters: '@'."
        )

    local, domain = email.split("@", 1)

    if not local:
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The part before the @-sign must not be empty."
        )

    if not domain:
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The domain must not be empty."
        )

    if not _LOCAL_RE.match(local):
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The part before the @-sign contains invalid characters."
        )

    if "." not in domain:
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The domain must contain a period."
        )

    labels = domain.split(".")
    tld = labels[-1]

    if not _TLD_RE.match(tld):
        raise EmailNotValidError(
            f"Invalid email address: {email!r}: The TLD must be at least 2 letters."
        )

    for label in labels[:-1]:
        if not label:
            raise EmailNotValidError(
                f"Invalid email address: {email!r}: The domain contains consecutive dots."
            )
        if not _LABEL_RE.match(label):
            raise EmailNotValidError(
                f"Invalid email address: {email!r}: The domain contains invalid characters."
            )


def is_valid_email(email: object) -> bool:
    """Return True if *email* is a well-formed email address, False otherwise."""
    try:
        _check_email(email)
        return True
    except EmailNotValidError:
        return False


def validate_email(email: object) -> str:
    """Return *email* unchanged if it is valid, otherwise raise EmailNotValidError."""
    _check_email(email)
    return email  # type: ignore[return-value]
