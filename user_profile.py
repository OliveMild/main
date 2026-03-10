#!/usr/bin/env python3
"""User profile module providing UserProfile class with error handling."""


class UserProfileError(Exception):
    """Raised when a user profile operation fails."""


class UserProfile:
    """Represents a user profile with basic attributes."""

    def __init__(self, username: str, email: str, display_name: str = ""):
        if not username or not username.strip():
            raise UserProfileError("Username cannot be empty")
        self._validate_email(email)
        self.username = username.strip()
        self.email = email.strip()
        self.display_name = display_name.strip() if display_name else self.username

    @staticmethod
    def _validate_email(email: str):
        """Validate an email address, raising UserProfileError if invalid."""
        if not email or "@" not in email:
            raise UserProfileError("Email address is empty or missing @ symbol")

    def update(self, email: str = None, display_name: str = None):
        """Update profile fields."""
        if email is not None:
            self._validate_email(email)
            self.email = email.strip()
        if display_name is not None:
            self.display_name = display_name.strip() if display_name.strip() else self.username

    def to_dict(self) -> dict:
        """Return profile as a dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
        }

    def __repr__(self) -> str:
        return f"UserProfile(username={self.username!r}, email={self.email!r}, display_name={self.display_name!r})"
