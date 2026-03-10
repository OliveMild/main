class UserProfileError(Exception):
    """Raised when a UserProfile operation fails validation."""


_VALID_FIELDS = {"username", "email"}


def _validate_username(username: str) -> None:
    if not (3 <= len(username) <= 30):
        raise UserProfileError("Username must be between 3 and 30 characters.")


def _normalize_email(email: str) -> str:
    if not email:
        raise UserProfileError("Email must not be empty.")
    return email.lower()


class UserProfile:
    """A simple user profile with validated username and normalized email."""

    def __init__(self, username: str, email: str) -> None:
        _validate_username(username)
        self._username = username
        self._email = _normalize_email(email)

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    def update(self, **kwargs) -> None:
        unknown = set(kwargs) - _VALID_FIELDS
        if unknown:
            raise UserProfileError(
                f"Unknown profile field(s): {', '.join(sorted(unknown))}"
            )
        if "username" in kwargs:
            _validate_username(kwargs["username"])
            self._username = kwargs["username"]
        if "email" in kwargs:
            self._email = _normalize_email(kwargs["email"])
