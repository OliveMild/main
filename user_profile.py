#!/usr/bin/env python3
"""User profile module with error handling."""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserProfileError(Exception):
    """Base exception for user profile errors."""


class UserNotFoundError(UserProfileError):
    """Raised when a user profile cannot be found."""

    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User profile not found: {user_id}")


class InvalidProfileDataError(UserProfileError):
    """Raised when profile data fails validation."""

    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Invalid profile data for '{field}': {message}")


class UserProfile:
    """Represents a user profile."""

    REQUIRED_FIELDS = ("name", "email")

    def __init__(self, user_id, name, email, bio=""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.bio = bio

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "bio": self.bio,
        }

    def __repr__(self):
        return f"UserProfile(user_id={self.user_id!r}, name={self.name!r}, email={self.email!r})"


class UserProfileStore:
    """In-memory store for user profiles."""

    def __init__(self):
        self._profiles = {}

    def _validate(self, data):
        for field in UserProfile.REQUIRED_FIELDS:
            if not data.get(field):
                raise InvalidProfileDataError(field, "field is required and cannot be empty")
        if not _EMAIL_RE.match(data["email"]):
            raise InvalidProfileDataError("email", "must be a valid email address (e.g. user@example.com)")

    def create(self, user_id, name, email, bio=""):
        self._validate({"name": name, "email": email})
        if user_id in self._profiles:
            raise UserProfileError(f"Profile already exists for user: {user_id}")
        profile = UserProfile(user_id, name, email, bio)
        self._profiles[user_id] = profile
        return profile

    def get(self, user_id):
        try:
            return self._profiles[user_id]
        except KeyError:
            raise UserNotFoundError(user_id)

    def update(self, user_id, **kwargs):
        profile = self.get(user_id)
        updated = {**profile.to_dict(), **kwargs}
        self._validate(updated)
        profile.name = updated["name"]
        profile.email = updated["email"]
        profile.bio = updated["bio"]
        return profile

    def delete(self, user_id):
        if user_id not in self._profiles:
            raise UserNotFoundError(user_id)
        return self._profiles.pop(user_id)
