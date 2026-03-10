#!/usr/bin/env python3

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(email):
    if not email or not _EMAIL_RE.match(email):
        raise ValidationError("email must be a valid email address")


class ValidationError(Exception):
    pass


class ProfileNotFoundError(Exception):
    pass


class UserProfile:
    def __init__(self, user_id, name, email, bio=""):
        if not user_id:
            raise ValidationError("user_id cannot be empty")
        if not name or not name.strip():
            raise ValidationError("name cannot be empty")
        _validate_email(email)
        self.user_id = user_id
        self.name = name.strip()
        self.email = email
        self.bio = bio

    def update(self, name=None, email=None, bio=None):
        if name is not None:
            if not name.strip():
                raise ValidationError("name cannot be empty")
            self.name = name.strip()
        if email is not None:
            _validate_email(email)
            self.email = email
        if bio is not None:
            self.bio = bio

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "bio": self.bio,
        }


class UserProfileStore:
    def __init__(self):
        self._profiles = {}

    def add(self, profile):
        if profile.user_id in self._profiles:
            raise ValidationError(f"Profile with user_id '{profile.user_id}' already exists")
        self._profiles[profile.user_id] = profile

    def get(self, user_id):
        if user_id not in self._profiles:
            raise ProfileNotFoundError(f"Profile with user_id '{user_id}' not found")
        return self._profiles[user_id]

    def update(self, user_id, name=None, email=None, bio=None):
        profile = self.get(user_id)
        profile.update(name=name, email=email, bio=bio)
        return profile

    def delete(self, user_id):
        if user_id not in self._profiles:
            raise ProfileNotFoundError(f"Profile with user_id '{user_id}' not found")
        del self._profiles[user_id]

    def list_all(self):
        return list(self._profiles.values())
