#!/usr/bin/env python3
"""User profile module for managing user profile data."""

import re


class ProfileError(Exception):
    """Raised when a user profile operation fails."""


_VALID_FIELDS = {"username", "email", "bio", "location", "website"}
_EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')


def _validate_username(username):
    if not isinstance(username, str) or not username.strip():
        raise ProfileError("Username must be a non-empty string.")
    if len(username.strip()) > 50:
        raise ProfileError("Username must be 50 characters or fewer.")


def _validate_email(email):
    if not isinstance(email, str) or not email.strip():
        raise ProfileError("Email must be a non-empty string.")
    if not _EMAIL_PATTERN.match(email.strip()):
        raise ProfileError("Invalid email address.")


def create_profile(username, email, bio="", location="", website=""):
    """Create a new user profile.

    Args:
        username: The user's display name (required, max 50 chars).
        email: The user's email address (required, must be valid).
        bio: Optional short biography.
        location: Optional location string.
        website: Optional website URL.

    Returns:
        A dict representing the new user profile.

    Raises:
        ProfileError: If any field is invalid.
    """
    _validate_username(username)
    _validate_email(email)

    return {
        "username": username.strip(),
        "email": email.strip(),
        "bio": bio.strip() if isinstance(bio, str) else "",
        "location": location.strip() if isinstance(location, str) else "",
        "website": website.strip() if isinstance(website, str) else "",
    }


def update_profile(profile, **fields):
    """Update fields on an existing user profile.

    Args:
        profile: The existing profile dict to update.
        **fields: Keyword arguments for fields to update.
                  Supported fields: username, email, bio, location, website.

    Returns:
        A new dict with the updated profile.

    Raises:
        ProfileError: If the profile is invalid or any updated field is invalid.
        ValueError: If an unsupported field name is provided.
    """
    if not isinstance(profile, dict):
        raise ProfileError("Profile must be a dict.")

    unknown = set(fields) - _VALID_FIELDS
    if unknown:
        raise ValueError(f"Unsupported profile field(s): {', '.join(sorted(unknown))}")

    updated = dict(profile)

    if "username" in fields:
        _validate_username(fields["username"])
        updated["username"] = fields["username"].strip()

    if "email" in fields:
        _validate_email(fields["email"])
        updated["email"] = fields["email"].strip()

    for field in ("bio", "location", "website"):
        if field in fields:
            value = fields[field]
            updated[field] = value.strip() if isinstance(value, str) else ""

    return updated


def get_display_name(profile):
    """Return the display name for a profile.

    Args:
        profile: A profile dict.

    Returns:
        The username string, or 'Unknown User' if the profile is missing a username.
    """
    if not isinstance(profile, dict):
        return "Unknown User"
    name = profile.get("username", "")
    return name.strip() if isinstance(name, str) and name.strip() else "Unknown User"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: user_profile.py <username> <email> [bio]")
        sys.exit(1)

    bio_arg = sys.argv[3] if len(sys.argv) > 3 else ""
    try:
        p = create_profile(sys.argv[1], sys.argv[2], bio=bio_arg)
        print(f"Profile created for {get_display_name(p)} ({p['email']})")
    except ProfileError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
