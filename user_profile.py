"""User profile management with file persistence."""

import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".user_profile.json")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_profile(name, email, path=_DEFAULT_PROFILE_PATH):
    """Create a new user profile and persist it to *path*.

    Args:
        name: The user's display name. Must not be empty.
        email: The user's email address. Must be a valid email address.
        path: Destination file path for the JSON profile.

    Raises:
        ValueError: If *name* is empty or *email* is not a valid email address.
    """
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")

    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)


def load_profile(path=_DEFAULT_PROFILE_PATH):
    """Load a user profile from *path*.

    Args:
        path: Source file path for the JSON profile.

    Returns:
        A dict with at least ``name`` and ``email`` keys.

    Raises:
        FileNotFoundError: If *path* does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No profile found at {path!r}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def update_profile(updates, path=_DEFAULT_PROFILE_PATH):
    """Merge *updates* into the existing profile at *path*.

    Args:
        updates: A dict of fields to update in the profile.
        path: File path of the JSON profile to update.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: If *updates* contains an empty ``name`` or an invalid
            ``email``.
    """
    profile = load_profile(path)

    if "name" in updates and not updates["name"]:
        raise ValueError("name must not be empty")
    if "email" in updates and not _EMAIL_RE.match(updates["email"]):
        raise ValueError("email must be a valid email address")

    profile.update(updates)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
