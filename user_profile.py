#!/usr/bin/env python3
"""User profile management module."""

import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".user_profile.json")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_name(name):
    if not name or not name.strip():
        raise ValueError("name must not be empty")


def _validate_email(email):
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")


def create_profile(name, email, path=None):
    """Create a new user profile.

    Args:
        name: The user's name. Must not be empty.
        email: The user's email address. Must be a valid email.
        path: Optional file path to store the profile. Defaults to ~/.user_profile.json.

    Raises:
        ValueError: If name is empty or email is not a valid email address.
    """
    _validate_name(name)
    _validate_email(email)
    profile = {"name": name, "email": email}
    profile_path = path or _DEFAULT_PROFILE_PATH
    with open(profile_path, "w") as f:
        json.dump(profile, f)
    return profile


def load_profile(path=None):
    """Load an existing user profile.

    Args:
        path: Optional file path to load the profile from. Defaults to ~/.user_profile.json.

    Returns:
        A dict with the user profile data.

    Raises:
        FileNotFoundError: If the profile file does not exist at the given path.
    """
    profile_path = path or _DEFAULT_PROFILE_PATH
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"No profile found at {profile_path!r}")
    with open(profile_path) as f:
        return json.load(f)


def update_profile(updates, path=None):
    """Update an existing user profile with the given fields.

    Args:
        updates: A dict of fields to update in the profile.
        path: Optional file path to the profile file. Defaults to ~/.user_profile.json.

    Returns:
        The updated profile dict.

    Raises:
        FileNotFoundError: If the profile file does not exist at the given path.
        ValueError: If updated name is empty or updated email is not valid.
    """
    profile = load_profile(path)
    if "name" in updates:
        _validate_name(updates["name"])
    if "email" in updates:
        _validate_email(updates["email"])
    profile.update(updates)
    profile_path = path or _DEFAULT_PROFILE_PATH
    with open(profile_path, "w") as f:
        json.dump(profile, f)
    return profile
