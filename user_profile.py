import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@.\s][^@\s]*\.[^@\s.]+$")


class UserProfileError(Exception):
    pass


class UserProfile:
    _VALID_FIELDS = {"username", "email"}

    @staticmethod
    def _validate_username(username: str) -> None:
        if not (3 <= len(username) <= 30):
            raise UserProfileError("Username must be between 3 and 30 characters.")

    @staticmethod
    def _validate_email(email: str) -> None:
        if not _EMAIL_RE.match(email):
            raise UserProfileError(f"Invalid email address: {email!r}")

    def __init__(self, username: str, email: str) -> None:
        self._validate_username(username)
        self._validate_email(email)
        self.username = username
        self.email = email.lower()

    def update(self, **kwargs) -> None:
        unknown = set(kwargs) - self._VALID_FIELDS
        if unknown:
            fields = ", ".join(sorted(unknown))
            raise UserProfileError(f"Unknown profile field(s): {fields}")
        if "username" in kwargs:
            self._validate_username(kwargs["username"])
            self.username = kwargs["username"]
        if "email" in kwargs:
            self._validate_email(kwargs["email"])
            self.email = kwargs["email"].lower()
