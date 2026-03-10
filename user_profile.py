import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")


def create_profile(name: str, email: str, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Create a new user profile and persist it to *path*.

    Raises:
        ValueError: if *name* is empty or *email* is not a valid email address.
    """
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")

    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f)


def load_profile(path: str = _DEFAULT_PROFILE_PATH) -> dict:
    """Load a user profile from *path*.

    Raises:
        FileNotFoundError: if *path* does not exist.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No profile found at '{path}'") from e


def update_profile(updates: dict, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Apply *updates* to the existing profile stored at *path* and save it.

    Raises:
        ValueError: if *updates* contains an empty 'name' or an invalid 'email'.
        FileNotFoundError: if the profile at *path* does not exist.
    """
    if "name" in updates and not updates["name"]:
        raise ValueError("name must not be empty")
    if "email" in updates and not _EMAIL_RE.match(updates["email"]):
        raise ValueError("email must be a valid email address")

    profile = load_profile(path)
    profile.update(updates)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f)
