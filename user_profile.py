#!/usr/bin/env python3
"""User profile module providing basic profile management."""


class UserProfileNotFoundError(Exception):
    """Raised when a user profile cannot be found."""


class UserProfile:
    """Represents a user profile with basic attributes."""

    def __init__(self, user_id, name, email, bio=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.bio = bio or ""

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

    def add(self, profile: UserProfile) -> None:
        """Add or update a user profile in the store."""
        self._profiles[profile.user_id] = profile

    def get(self, user_id) -> UserProfile:
        """Return the profile for the given user_id.

        Raises:
            UserProfileNotFoundError: if no profile exists for user_id.
        """
        profile = self._profiles.get(user_id)
        if profile is None:
            raise UserProfileNotFoundError(
                f"No profile found for user_id={user_id!r}"
            )
        return profile

    _UPDATABLE_FIELDS = frozenset({"name", "email", "bio"})

    def update(self, user_id, **kwargs) -> UserProfile:
        """Update mutable fields on an existing profile and return it.

        Only ``name``, ``email``, and ``bio`` may be changed.

        Raises:
            UserProfileNotFoundError: if no profile exists for user_id.
            AttributeError: if a key outside the allowed fields is supplied.
        """
        profile = self.get(user_id)
        for key, value in kwargs.items():
            if key not in self._UPDATABLE_FIELDS:
                raise AttributeError(
                    f"UserProfile field {key!r} cannot be updated"
                )
            setattr(profile, key, value)
        return profile

    def delete(self, user_id) -> None:
        """Remove a profile from the store.

        Raises:
            UserProfileNotFoundError: if no profile exists for user_id.
        """
        if user_id not in self._profiles:
            raise UserProfileNotFoundError(
                f"No profile found for user_id={user_id!r}"
            )
        del self._profiles[user_id]

    def all(self) -> list[UserProfile]:
        """Return a list of all stored profiles."""
        return list(self._profiles.values())
