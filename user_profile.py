#!/usr/bin/env python3

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserProfileError(Exception):
    """Base exception for user profile errors."""


class UserNotFoundError(UserProfileError):
    """Raised when a user profile is not found."""


class InvalidFieldError(UserProfileError):
    """Raised when an invalid field is provided."""


ALLOWED_FIELDS = {"name", "email", "age", "bio"}


def _validate_email(email):
    """Raise UserProfileError if email is not valid."""
    if not email or not _EMAIL_RE.match(email):
        raise UserProfileError("email must be a valid email address")


def _validate_age(age):
    """Raise UserProfileError if age is not valid."""
    if age is not None and (not isinstance(age, int) or age < 0):
        raise UserProfileError("age must be a non-negative integer")


class UserProfile:
    """Represents a user profile with basic attributes."""

    def __init__(self, user_id, name, email, age=None, bio=""):
        if not user_id:
            raise UserProfileError("user_id cannot be empty")
        if not name:
            raise UserProfileError("name cannot be empty")
        _validate_email(email)
        _validate_age(age)

        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.bio = bio

    def update(self, **kwargs):
        """Update allowed profile fields."""
        invalid = set(kwargs) - ALLOWED_FIELDS
        if invalid:
            raise InvalidFieldError(f"Invalid fields: {invalid}")

        if "email" in kwargs:
            _validate_email(kwargs["email"])
        if "age" in kwargs:
            _validate_age(kwargs["age"])

        for field, value in kwargs.items():
            setattr(self, field, value)

    def to_dict(self):
        """Return the profile as a dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "bio": self.bio,
        }

    def __repr__(self):
        return f"UserProfile(user_id={self.user_id!r}, name={self.name!r}, email={self.email!r})"


class UserProfileStore:
    """In-memory store for user profiles."""

    def __init__(self):
        self._profiles = {}

    def add(self, profile):
        """Add a user profile to the store."""
        if not isinstance(profile, UserProfile):
            raise UserProfileError("Expected a UserProfile instance")
        self._profiles[profile.user_id] = profile

    def get(self, user_id):
        """Retrieve a user profile by user_id."""
        if user_id not in self._profiles:
            raise UserNotFoundError(f"No profile found for user_id={user_id!r}")
        return self._profiles[user_id]

    def delete(self, user_id):
        """Delete a user profile by user_id."""
        if user_id not in self._profiles:
            raise UserNotFoundError(f"No profile found for user_id={user_id!r}")
        del self._profiles[user_id]

    def all(self):
        """Return all stored profiles as a list."""
        return list(self._profiles.values())
