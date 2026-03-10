"""User profile management: create, load, and update a profile stored as JSON."""

import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

_EMAIL_RE = re.compile(r"^[^@\s]+@([^@\s.]+\.)+[^@\s.]+$")


def _validate(name: str, email: str) -> None:
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")


def create_profile(name: str, email: str, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Create a new profile and save it to *path* (default: profile.json)."""
    _validate(name, email)
    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f)


def load_profile(path: str = _DEFAULT_PROFILE_PATH) -> dict:
    """Load a profile from *path* (default: profile.json).

    Raises FileNotFoundError if *path* does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No profile found at '{path}'")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_profile(updates: dict, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Merge *updates* into the existing profile saved at *path*."""
    profile = load_profile(path)
    merged = {**profile, **updates}
    _validate(merged["name"], merged["email"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged, f)
