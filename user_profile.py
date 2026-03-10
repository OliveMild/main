#!/usr/bin/env python3
"""User profile module for managing user profile data."""

import re

_EMAIL_RE = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$'
)


class UserProfileError(Exception):
    """Raised when a user profile operation fails."""


class UserProfile:
    """Represents a user's profile with basic information."""

    def __init__(self, username, email, bio=""):
        """Initialise a UserProfile.

        Args:
            username: Non-empty string username.
            email: Valid email address string.
            bio: Optional biography string (default empty).

        Raises:
            UserProfileError: If any argument is invalid.
        """
        self._username = _validate_username(username)
        self._email = _validate_email(email)
        self._bio = _validate_bio(bio)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def bio(self):
        return self._bio

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get_profile(self):
        """Return a dict representation of the profile.

        Returns:
            dict with keys 'username', 'email', and 'bio'.
        """
        return {
            "username": self._username,
            "email": self._email,
            "bio": self._bio,
        }

    def update_profile(self, username=None, email=None, bio=None):
        """Update one or more profile fields.

        Only the fields provided (not None) are updated.

        Args:
            username: New username string (optional).
            email: New email address string (optional).
            bio: New biography string (optional).

        Raises:
            UserProfileError: If a provided value is invalid.
        """
        if username is not None:
            self._username = _validate_username(username)
        if email is not None:
            self._email = _validate_email(email)
        if bio is not None:
            self._bio = _validate_bio(bio)

    def __repr__(self):
        return (
            f"UserProfile(username={self._username!r}, "
            f"email={self._email!r}, bio={self._bio!r})"
        )


# ------------------------------------------------------------------
# Internal validation helpers
# ------------------------------------------------------------------

def _validate_username(username):
    """Return the validated username string.

    Raises:
        UserProfileError: If the username is invalid.
    """
    if not isinstance(username, str):
        raise UserProfileError("Username must be a string.")
    username = username.strip()
    if not username:
        raise UserProfileError("Username must not be empty.")
    if len(username) > 50:
        raise UserProfileError("Username must not exceed 50 characters.")
    return username


def _validate_email(email):
    """Return the validated email address string.

    Raises:
        UserProfileError: If the email is invalid.
    """
    if not isinstance(email, str):
        raise UserProfileError("Email must be a string.")
    email = email.strip()
    if not email:
        raise UserProfileError("Email must not be empty.")
    if len(email) > 320:
        raise UserProfileError("Email must not exceed 320 characters.")
    if ' ' in email:
        raise UserProfileError("Email must not contain spaces.")
    if email.count('@') != 1:
        raise UserProfileError("Email must contain exactly one '@' character.")
    _, domain = email.split('@')
    if '..' in domain:
        raise UserProfileError("Email domain must not contain consecutive dots.")
    if not _EMAIL_RE.match(email):
        raise UserProfileError(f"Invalid email address: {email!r}.")
    return email


def _validate_bio(bio):
    """Return the validated bio string.

    Raises:
        UserProfileError: If the bio is invalid.
    """
    if not isinstance(bio, str):
        raise UserProfileError("Bio must be a string.")
    if len(bio) > 500:
        raise UserProfileError("Bio must not exceed 500 characters.")
    return bio

