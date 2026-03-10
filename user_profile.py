#!/usr/bin/env python3
"""User profile module."""

import re
from typing import Optional


class ValidationError(Exception):
    """Raised when a profile field fails validation."""


_DISPLAY_NAME_MAX = 100
_BIO_MAX = 500
_USERNAME_MAX = 50
_URL_PATTERN = re.compile(
    r"^https?://"                                       # scheme: http or https
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}"  # domain
    r"(?::\d+)?(?:/[^\s]*)?$"                           # optional port and path
)


def _validate_username(username: str) -> None:
    if not username or not username.strip():
        raise ValidationError("Username must not be empty.")
    if len(username) > _USERNAME_MAX:
        raise ValidationError(f"Username must not exceed {_USERNAME_MAX} characters.")
    if " " in username:
        raise ValidationError("Username must not contain whitespace.")


def _validate_display_name(display_name: str) -> None:
    if not display_name or not display_name.strip():
        raise ValidationError("Display name must not be empty.")
    if len(display_name) > _DISPLAY_NAME_MAX:
        raise ValidationError(
            f"Display name must not exceed {_DISPLAY_NAME_MAX} characters."
        )


def _validate_bio(bio: str) -> None:
    if len(bio) > _BIO_MAX:
        raise ValidationError(f"Bio must not exceed {_BIO_MAX} characters.")


def _validate_avatar_url(avatar_url: str) -> None:
    if avatar_url and not _URL_PATTERN.match(avatar_url):
        raise ValidationError("Avatar URL must be a valid http or https URL.")


class UserProfile:
    """Represents a user's public profile."""

    def __init__(
        self,
        username: str,
        display_name: str,
        bio: str = "",
        avatar_url: str = "",
    ) -> None:
        _validate_username(username)
        _validate_display_name(display_name)
        _validate_bio(bio)
        _validate_avatar_url(avatar_url)
        self.username = username
        self.display_name = display_name
        self.bio = bio
        self.avatar_url = avatar_url

    def update(
        self,
        display_name: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> None:
        """Update profile fields.  Only provided (non-None) fields are changed.

        Raises:
            ValidationError: If any supplied value fails validation.
        """
        new_display_name = display_name if display_name is not None else self.display_name
        new_bio = bio if bio is not None else self.bio
        new_avatar_url = avatar_url if avatar_url is not None else self.avatar_url

        _validate_display_name(new_display_name)
        _validate_bio(new_bio)
        _validate_avatar_url(new_avatar_url)

        self.display_name = new_display_name
        self.bio = new_bio
        self.avatar_url = new_avatar_url

    def __repr__(self) -> str:
        return (
            f"UserProfile(username={self.username!r}, "
            f"display_name={self.display_name!r})"
        )


class ProfileManager:
    """Manages a collection of user profiles."""

    def __init__(self) -> None:
        self._profiles: dict[str, UserProfile] = {}

    def create_profile(
        self,
        username: str,
        display_name: str,
        bio: str = "",
        avatar_url: str = "",
    ) -> UserProfile:
        """Create and store a new profile.

        Raises:
            ValidationError: If any field fails validation.
            ValueError: If a profile for *username* already exists.
        """
        key = username.lower()
        if key in self._profiles:
            raise ValueError(f"Profile for '{username}' already exists.")

        profile = UserProfile(username, display_name, bio, avatar_url)
        self._profiles[key] = profile
        return profile

    def get_profile(self, username: str) -> Optional[UserProfile]:
        """Return the profile for *username*, or None if not found."""
        return self._profiles.get(username.lower())

    def delete_profile(self, username: str) -> bool:
        """Delete the profile for *username*.  Return True if it existed."""
        return self._profiles.pop(username.lower(), None) is not None

    def __len__(self) -> int:
        return len(self._profiles)
