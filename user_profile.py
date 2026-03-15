#!/usr/bin/env python3
"""User profile module with error handling."""


class UserProfileError(Exception):
    """Base exception for user profile errors."""


class MissingFieldError(UserProfileError):
    """Raised when a required field is missing from the user profile."""

    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"Missing required field: '{field_name}'")


class InvalidFieldError(UserProfileError):
    """Raised when a field value is invalid."""

    def __init__(self, field_name, reason):
        self.field_name = field_name
        self.reason = reason
        super().__init__(f"Invalid value for '{field_name}': {reason}")


class UserProfile:
    """Represents a user profile with validation."""

    REQUIRED_FIELDS = ("username", "email")
    UPDATABLE_FIELDS = frozenset({"email", "display_name", "bio"})

    def __init__(self, username, email, display_name=None, bio=None):
        self._validate_username(username)
        self._validate_email(email)
        self.username = username
        self.email = email
        self.display_name = display_name or username
        self.bio = bio or ""

    @staticmethod
    def _validate_username(username):
        if not username:
            raise MissingFieldError("username")
        if not isinstance(username, str):
            raise InvalidFieldError("username", "must be a string")
        if len(username) < 3:
            raise InvalidFieldError("username", "must be at least 3 characters long")
        if len(username) > 50:
            raise InvalidFieldError("username", "must not exceed 50 characters")
        if not username.replace("_", "").replace("-", "").isalnum():
            raise InvalidFieldError(
                "username", "may only contain letters, digits, hyphens, and underscores"
            )

    @staticmethod
    def _validate_email(email):
        if not email:
            raise MissingFieldError("email")
        if not isinstance(email, str):
            raise InvalidFieldError("email", "must be a string")
        if "@" not in email or email.count("@") != 1:
            raise InvalidFieldError("email", "must contain exactly one '@' character")
        local, domain = email.split("@")
        if not local:
            raise InvalidFieldError("email", "local part must not be empty")
        if not domain or "." not in domain:
            raise InvalidFieldError("email", "domain part must contain at least one '.'")

    def update(self, **kwargs):
        """Update profile fields with validation."""
        for key, value in kwargs.items():
            if key not in self.UPDATABLE_FIELDS:
                raise InvalidFieldError(key, "field cannot be updated")
            if key == "email":
                self._validate_email(value)
            setattr(self, key, value)

    def to_dict(self):
        """Return profile data as a dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "bio": self.bio,
        }

    def __repr__(self):
        return f"UserProfile(username={self.username!r}, email={self.email!r})"
