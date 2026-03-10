import json
import os
import re

DEFAULT_PROFILE_PATH = "profile.json"

_EMAIL_RE = re.compile(r'^[^@\s]+@[A-Za-z0-9]([A-Za-z0-9\-]*[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9\-]*[A-Za-z0-9])?)*\.[A-Za-z]{2,}$')


def create_profile(name, email, path=DEFAULT_PROFILE_PATH):
    """Create a new user profile and persist it to *path* as JSON.

    Raises:
        ValueError: if *name* is empty or *email* is not a valid email address.
    """
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")

    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh)
    return profile


def load_profile(path=DEFAULT_PROFILE_PATH):
    """Load a user profile from *path* and return it as a dict.

    Raises:
        FileNotFoundError: if *path* does not exist.
    """
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def update_profile(updates, path=DEFAULT_PROFILE_PATH):
    """Apply *updates* to the existing profile stored at *path* and save it.

    Raises:
        FileNotFoundError: if *path* does not exist.
        ValueError: if *updates* contains an empty name or invalid email address.
    """
    if "name" in updates and not updates["name"]:
        raise ValueError("name must not be empty")
    if "email" in updates and not _EMAIL_RE.match(updates["email"]):
        raise ValueError("email must be a valid email address")

    profile = load_profile(path)
    profile.update(updates)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh)
    return profile
