#!/usr/bin/env python3
"""User profile module with CRUD operations and typed exception hierarchy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class UserProfileError(Exception):
    """Base exception for user profile operations."""


class UserNotFoundError(UserProfileError):
    """Raised when a requested user does not exist."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User with id {user_id!r} not found")


class DuplicateUsernameError(UserProfileError):
    """Raised when a username is already taken."""

    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"Username {username!r} is already taken")


class InvalidProfileDataError(UserProfileError):
    """Raised when profile data fails validation."""


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class UserProfile:
    """Represents a user profile."""

    id: int
    username: str
    email: str
    bio: str = ""
    avatar_url: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
        }


# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------


@dataclass
class UserProfileStore:
    """Simple in-memory store for user profiles."""

    _profiles: Dict[int, UserProfile] = field(default_factory=dict)
    _next_id: int = 1

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _validate(self, username: str, email: str) -> None:
        if not username or not username.strip():
            raise InvalidProfileDataError("username must not be empty")
        if not email or "@" not in email:
            raise InvalidProfileDataError("email must be a valid address")

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(self, username: str, email: str, bio: str = "", avatar_url: str = "") -> UserProfile:
        """Create a new user profile and return it."""
        self._validate(username, email)
        for profile in self._profiles.values():
            if profile.username == username:
                raise DuplicateUsernameError(username)
        profile = UserProfile(
            id=self._next_id,
            username=username,
            email=email,
            bio=bio,
            avatar_url=avatar_url,
        )
        self._profiles[self._next_id] = profile
        self._next_id += 1
        return profile

    def get(self, user_id: int) -> UserProfile:
        """Return the profile with the given ID."""
        profile = self._profiles.get(user_id)
        if profile is None:
            raise UserNotFoundError(user_id)
        return profile

    def list_all(self) -> list[UserProfile]:
        """Return all profiles."""
        return list(self._profiles.values())

    def update(
        self,
        user_id: int,
        *,
        username: Optional[str] = None,
        email: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> UserProfile:
        """Update an existing profile and return the updated version."""
        profile = self.get(user_id)
        new_username = username if username is not None else profile.username
        new_email = email if email is not None else profile.email
        self._validate(new_username, new_email)
        if username is not None and username != profile.username:
            for p in self._profiles.values():
                if p.username == username and p.id != user_id:
                    raise DuplicateUsernameError(username)
        profile.username = new_username
        profile.email = new_email
        if bio is not None:
            profile.bio = bio
        if avatar_url is not None:
            profile.avatar_url = avatar_url
        return profile

    def delete(self, user_id: int) -> None:
        """Delete the profile with the given ID."""
        if user_id not in self._profiles:
            raise UserNotFoundError(user_id)
        del self._profiles[user_id]
