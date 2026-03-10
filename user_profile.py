#!/usr/bin/env python3
"""User profile module with validation and error handling."""

import re


class UserProfileError(Exception):
    """Base exception for user profile errors."""


class InvalidEmailError(UserProfileError):
    """Raised when an invalid email address is provided."""


class InvalidUsernameError(UserProfileError):
    """Raised when an invalid username is provided."""


class InvalidAgeError(UserProfileError):
    """Raised when an invalid age is provided."""


class UserProfile:
    """Represents a user profile with validation."""

    _EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")

    def __init__(self, username: str, email: str, age: int | None = None):
        self.username = username
        self.email = email
        self.age = age

    # ------------------------------------------------------------------
    # username
    # ------------------------------------------------------------------
    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        if not isinstance(value, str) or not self._USERNAME_RE.match(value):
            raise InvalidUsernameError(
                f"Username '{value}' is invalid. "
                "Usernames must be 3–30 characters and contain only "
                "letters, digits, or underscores."
            )
        self._username = value

    # ------------------------------------------------------------------
    # email
    # ------------------------------------------------------------------
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str) or not self._EMAIL_RE.match(value):
            raise InvalidEmailError(
                f"Email '{value}' is not a valid email address."
            )
        self._email = value

    # ------------------------------------------------------------------
    # age
    # ------------------------------------------------------------------
    @property
    def age(self) -> int | None:
        return self._age

    @age.setter
    def age(self, value: int | None) -> None:
        if value is not None and (not isinstance(value, int) or value < 0 or value > 150):
            raise InvalidAgeError(
                f"Age '{value}' is invalid. Age must be an integer between 0 and 150."
            )
        self._age = value

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def update(self, **kwargs) -> None:
        """Update profile fields by keyword argument."""
        _allowed = {"username", "email", "age"}
        for field, value in kwargs.items():
            if field not in _allowed:
                raise UserProfileError(f"Unknown profile field: '{field}'")
            setattr(self, field, value)

    def to_dict(self) -> dict:
        """Return profile data as a dictionary."""
        return {
            "username": self._username,
            "email": self._email,
            "age": self._age,
        }

    def __repr__(self) -> str:
        return (
            f"UserProfile(username={self._username!r}, "
            f"email={self._email!r}, age={self._age!r})"
        )
