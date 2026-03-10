#!/usr/bin/env python3
"""User profile module with persistent JSON storage and error handling."""

import json
import os

DEFAULT_FILEPATH = "user_profile.json"

REQUIRED_FIELDS = {"name", "email"}


def _validate_email(email):
    """Validate that email is a non-empty string with a valid format.

    Raises:
        TypeError: If email is not a string.
        ValueError: If the email format is invalid.
    """
    if not isinstance(email, str):
        raise TypeError("email must be a string")
    if "@" not in email or not email.strip():
        raise ValueError("email must be a valid email address")
    local, _, domain = email.strip().partition("@")
    if not local or not domain or "@" in domain:
        raise ValueError("email must be a valid email address")


def create_profile(name, email, filepath=DEFAULT_FILEPATH):
    """Create and save a new user profile.

    Args:
        name: Non-empty string for the user's display name.
        email: Non-empty string containing '@' for the user's email address.
        filepath: Path to the JSON storage file.

    Raises:
        TypeError: If name or email is not a string.
        ValueError: If name is empty or email is not a valid address.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not name.strip():
        raise ValueError("name must not be empty")
    _validate_email(email)

    profile = {"name": name.strip(), "email": email.strip()}
    _save_profile(profile, filepath)
    return profile


def load_profile(filepath=DEFAULT_FILEPATH):
    """Load a user profile from the JSON store.

    Args:
        filepath: Path to the JSON storage file.

    Returns:
        A dict with the user profile data.

    Raises:
        FileNotFoundError: If no profile file exists at the given path.
        ValueError: If the file is corrupt or missing required fields.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No profile found at '{filepath}'")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            profile = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Profile file is corrupt or unreadable: {exc}") from exc

    missing = REQUIRED_FIELDS - profile.keys()
    if missing:
        raise ValueError(f"Profile is missing required fields: {sorted(missing)}")
    return profile


def update_profile(updates, filepath=DEFAULT_FILEPATH):
    """Update fields of an existing user profile.

    Args:
        updates: A dict of field names and new values.
        filepath: Path to the JSON storage file.

    Raises:
        TypeError: If updates is not a dict, or if a field value has the wrong type.
        ValueError: If the profile doesn't exist, a field value is invalid, or the
                    file is corrupt.
    """
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dict")
    profile = load_profile(filepath)

    if "name" in updates:
        name = updates["name"]
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name.strip():
            raise ValueError("name must not be empty")
        profile["name"] = name.strip()

    if "email" in updates:
        _validate_email(updates["email"])
        profile["email"] = updates["email"].strip()

    _save_profile(profile, filepath)
    return profile


def delete_profile(filepath=DEFAULT_FILEPATH):
    """Delete the user profile file.

    Args:
        filepath: Path to the JSON storage file.

    Raises:
        FileNotFoundError: If no profile file exists at the given path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No profile found at '{filepath}'")
    os.remove(filepath)


def _save_profile(profile, filepath):
    """Write profile dict to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
