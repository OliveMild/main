class UserProfileError(Exception):
    pass


class UserProfile:
    _VALID_FIELDS = {"username", "email"}

    def __init__(self, username: str, email: str):
        self._validate_username(username)
        self.username = username
        self.email = email.lower()

    @staticmethod
    def _validate_username(username: str):
        if not (3 <= len(username) <= 30):
            raise UserProfileError("Username must be between 3 and 30 characters.")

    def update(self, **kwargs):
        unknown = set(kwargs) - self._VALID_FIELDS
        if unknown:
            raise UserProfileError(
                f"Unknown profile field(s): {', '.join(sorted(unknown))}"
            )
        if "username" in kwargs:
            self._validate_username(kwargs["username"])
            self.username = kwargs["username"]
        if "email" in kwargs:
            self.email = kwargs["email"].lower()
