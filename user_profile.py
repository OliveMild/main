#!/usr/bin/env python3
"""User profile module providing profile creation and management."""

import re


class UserProfileError(Exception):
    """Raised when a user profile operation fails."""


class UserProfile:
    """Represents a user profile with validation.

    Attributes:
        username: The unique display name for the user.
        email: The user's email address.
        bio: An optional short description about the user.
    """

    def __init__(self, username: str, email: str, bio: str = "") -> None:
        """Create a new UserProfile.

        Args:
            username: Must be 3–30 characters, letters/digits/underscores only.
            email: A valid email address.
            bio: Optional biography (max 200 characters).

        Raises:
            UserProfileError: If any field fails validation.
        """
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.bio = self._validate_bio(bio)

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_username(username: str) -> str:
        """Return *username* if valid, otherwise raise UserProfileError."""
        if not isinstance(username, str):
            raise UserProfileError("Username must be a string.")
        username = username.strip()
        if not (3 <= len(username) <= 30):
            raise UserProfileError(
                "Username must be between 3 and 30 characters."
            )
        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            raise UserProfileError(
                "Username may only contain letters, digits, and underscores."
            )
        return username

    @staticmethod
    def _validate_email(email: str) -> str:
        """Return *email* if valid, otherwise raise UserProfileError."""
        if not isinstance(email, str):
            raise UserProfileError("Email must be a string.")
        email = email.strip().lower()
        pattern = r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$"
        if not re.fullmatch(pattern, email):
            raise UserProfileError(f"'{email}' is not a valid email address.")
        return email

    @staticmethod
    def _validate_bio(bio: str) -> str:
        """Return *bio* if valid, otherwise raise UserProfileError."""
        if not isinstance(bio, str):
            raise UserProfileError("Bio must be a string.")
        if len(bio) > 200:
            raise UserProfileError("Bio must not exceed 200 characters.")
        return bio

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update(self, **kwargs) -> None:
        """Update one or more profile fields.

        Keyword Args:
            username: New username value.
            email: New email value.
            bio: New bio value.

        Raises:
            UserProfileError: If an unsupported field is provided or a
                value fails validation.
        """
        allowed = {"username", "email", "bio"}
        unknown = set(kwargs) - allowed
        if unknown:
            raise UserProfileError(
                f"Unknown profile field(s): {', '.join(sorted(unknown))}"
            )
        if "username" in kwargs:
            self.username = self._validate_username(kwargs["username"])
        if "email" in kwargs:
            self.email = self._validate_email(kwargs["email"])
        if "bio" in kwargs:
            self.bio = self._validate_bio(kwargs["bio"])

    def to_dict(self) -> dict:
        """Return the profile as a plain dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
        }

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"UserProfile(username={self.username!r}, email={self.email!r})"
        )
