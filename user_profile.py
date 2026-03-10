import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".user_profile.json")

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def create_profile(name: str, email: str, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Create a new user profile and persist it to *path*."""
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")
    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh)


def load_profile(path: str = _DEFAULT_PROFILE_PATH) -> dict:
    """Load and return the user profile stored at *path*.

    Raises FileNotFoundError if *path* does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No profile found at '{path}'")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def update_profile(updates: dict, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Merge *updates* into the existing profile stored at *path*."""
    if "name" in updates and not updates["name"]:
        raise ValueError("name must not be empty")
    if "email" in updates and not _EMAIL_RE.match(updates["email"]):
        raise ValueError("email must be a valid email address")
    profile = load_profile(path)
    profile.update(updates)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh)
