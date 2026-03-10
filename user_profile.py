#!/usr/bin/env python3
"""User profile module for storing and managing user profile information."""

import re


class ProfileNotFoundError(Exception):
    """Raised when a requested user profile does not exist."""


class ValidationError(Exception):
    """Raised when profile input fails validation."""


_DISPLAY_NAME_MAX = 100
_BIO_MAX = 500
_AVATAR_URL_MAX = 2048


def _validate_user_id(user_id: str) -> None:
    if not user_id or not user_id.strip():
        raise ValidationError("user_id must not be empty.")


def _validate_display_name(display_name: str) -> None:
    stripped = display_name.strip()
    if not stripped:
        raise ValidationError("Display name must not be empty.")
    if len(stripped) > _DISPLAY_NAME_MAX:
        raise ValidationError(
            f"Display name must not exceed {_DISPLAY_NAME_MAX} characters."
        )


def _validate_bio(bio: str) -> None:
    # Bio is optional and may contain leading/trailing whitespace; only length is enforced.
    if len(bio) > _BIO_MAX:
        raise ValidationError(f"Bio must not exceed {_BIO_MAX} characters.")


def _validate_avatar_url(avatar_url: str) -> None:
    if not avatar_url:
        return
    if len(avatar_url) > _AVATAR_URL_MAX:
        raise ValidationError(
            f"Avatar URL must not exceed {_AVATAR_URL_MAX} characters."
        )
    if not re.match(r"^https?://", avatar_url):
        raise ValidationError("Avatar URL must start with http:// or https://.")


class UserProfile:
    """Represents a user's profile information."""

    def __init__(
        self,
        user_id: str,
        display_name: str,
        bio: str = "",
        avatar_url: str = "",
    ) -> None:
        self.user_id = user_id
        self.display_name = display_name
        self.bio = bio
        self.avatar_url = avatar_url

    def __repr__(self) -> str:
        return (
            f"UserProfile(user_id={self.user_id!r}, "
            f"display_name={self.display_name!r})"
        )


class UserProfileStore:
    """Manages a collection of user profiles."""

    def __init__(self) -> None:
        self._profiles: dict[str, UserProfile] = {}

    def create_profile(
        self,
        user_id: str,
        display_name: str,
        bio: str = "",
        avatar_url: str = "",
    ) -> UserProfile:
        """Create and store a new profile for *user_id*.

        Raises:
            ValidationError: If any input fails validation.
        """
        _validate_user_id(user_id)
        _validate_display_name(display_name)
        _validate_bio(bio)
        _validate_avatar_url(avatar_url)

        profile = UserProfile(
            user_id=user_id,
            display_name=display_name.strip(),
            bio=bio,
            avatar_url=avatar_url,
        )
        self._profiles[user_id] = profile
        return profile

    def get_profile(self, user_id: str) -> UserProfile:
        """Return the profile for *user_id*.

        Raises:
            ProfileNotFoundError: If no profile exists for *user_id*.
        """
        try:
            return self._profiles[user_id]
        except KeyError:
            raise ProfileNotFoundError(
                f"No profile found for user '{user_id}'."
            )

    def update_profile(
        self,
        user_id: str,
        display_name: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
    ) -> UserProfile:
        """Update fields on an existing profile and return the updated profile.

        Only the fields explicitly passed (not ``None``) are changed.

        Raises:
            ProfileNotFoundError: If no profile exists for *user_id*.
            ValidationError: If any of the new values fail validation.
        """
        profile = self.get_profile(user_id)

        if display_name is not None:
            _validate_display_name(display_name)
            profile.display_name = display_name.strip()
        if bio is not None:
            _validate_bio(bio)
            profile.bio = bio
        if avatar_url is not None:
            _validate_avatar_url(avatar_url)
            profile.avatar_url = avatar_url

        return profile

    def delete_profile(self, user_id: str) -> None:
        """Remove the profile for *user_id*.

        Raises:
            ProfileNotFoundError: If no profile exists for *user_id*.
        """
        if user_id not in self._profiles:
            raise ProfileNotFoundError(
                f"No profile found for user '{user_id}'."
            )
        del self._profiles[user_id]

    def __len__(self) -> int:
        return len(self._profiles)
