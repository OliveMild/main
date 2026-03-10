#!/usr/bin/env python3
"""User profile module: creation, validation, update, and retrieval."""

import re
from datetime import datetime, timezone


class UserProfileError(Exception):
    """Base exception for user profile errors."""


class InvalidUsernameError(UserProfileError):
    """Raised when a username is invalid."""


class InvalidEmailError(UserProfileError):
    """Raised when an email address is invalid."""


class InvalidDisplayNameError(UserProfileError):
    """Raised when a display name is invalid."""


class InvalidBioError(UserProfileError):
    """Raised when a bio is invalid."""


class ProfileNotFoundError(UserProfileError):
    """Raised when a requested profile does not exist."""


class DuplicateUsernameError(UserProfileError):
    """Raised when attempting to create a profile with an already-used username."""


_USERNAME_RE = re.compile(r'^[A-Za-z0-9_]{3,32}$')
_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 32
DISPLAY_NAME_MAX_LENGTH = 64
BIO_MAX_LENGTH = 500


def _validate_username(username):
    if not isinstance(username, str) or not _USERNAME_RE.match(username):
        raise InvalidUsernameError(
            f"username must be {USERNAME_MIN_LENGTH}–{USERNAME_MAX_LENGTH} characters "
            "and contain only letters, digits, or underscores."
        )


def _validate_email(email):
    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        raise InvalidEmailError(
            "email must be a valid address (e.g. user@example.com)."
        )


def _validate_display_name(display_name):
    if not isinstance(display_name, str):
        raise InvalidDisplayNameError("display_name must be a string.")
    if len(display_name) > DISPLAY_NAME_MAX_LENGTH:
        raise InvalidDisplayNameError(
            f"display_name must not exceed {DISPLAY_NAME_MAX_LENGTH} characters."
        )


def _validate_bio(bio):
    if not isinstance(bio, str):
        raise InvalidBioError("bio must be a string.")
    if len(bio) > BIO_MAX_LENGTH:
        raise InvalidBioError(
            f"bio must not exceed {BIO_MAX_LENGTH} characters."
        )


class UserProfile:
    """Represents a single user profile."""

    def __init__(self, username, email, display_name="", bio=""):
        _validate_username(username)
        _validate_email(email)
        _validate_display_name(display_name)
        _validate_bio(bio)
        self._username = username
        self._email = email
        self._display_name = display_name
        self._bio = bio
        self._created_at = datetime.now(timezone.utc)
        self._updated_at = self._created_at

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        _validate_email(value)
        self._email = value
        self._updated_at = datetime.now(timezone.utc)

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        _validate_display_name(value)
        self._display_name = value
        self._updated_at = datetime.now(timezone.utc)

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, value):
        _validate_bio(value)
        self._bio = value
        self._updated_at = datetime.now(timezone.utc)

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def to_dict(self):
        """Return a plain-dict serialisation of this profile."""
        return {
            "username": self._username,
            "email": self._email,
            "display_name": self._display_name,
            "bio": self._bio,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }

    def __repr__(self):
        return (
            f"UserProfile(username={self._username!r}, "
            f"email={self._email!r}, display_name={self._display_name!r})"
        )


class ProfileStore:
    """In-memory store for UserProfile objects."""

    def __init__(self):
        self._profiles = {}

    def create(self, username, email, display_name="", bio=""):
        """Create and store a new profile; returns the profile.

        Raises DuplicateUsernameError if *username* is already registered.
        """
        if username in self._profiles:
            raise DuplicateUsernameError(
                f"A profile with username {username!r} already exists."
            )
        profile = UserProfile(
            username=username,
            email=email,
            display_name=display_name,
            bio=bio,
        )
        self._profiles[username] = profile
        return profile

    def get(self, username):
        """Return the profile for *username*.

        Raises ProfileNotFoundError if no such profile exists.
        """
        _validate_username(username)
        if username not in self._profiles:
            raise ProfileNotFoundError(
                f"No profile found for username {username!r}."
            )
        return self._profiles[username]

    def update(self, username, email=None, display_name=None, bio=None):
        """Update fields on an existing profile and return it.

        Raises ProfileNotFoundError if no such profile exists.
        """
        profile = self.get(username)
        if email is not None:
            profile.email = email
        if display_name is not None:
            profile.display_name = display_name
        if bio is not None:
            profile.bio = bio
        return profile

    def delete(self, username):
        """Remove a profile from the store.

        Raises ProfileNotFoundError if no such profile exists.
        """
        self.get(username)
        del self._profiles[username]

    def get_all(self):
        """Return a list of all stored profiles."""
        return list(self._profiles.values())

    def __len__(self):
        return len(self._profiles)
