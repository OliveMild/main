import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.][^@\s]*\.[^@\s.][^@\s]*$")


def _validate(name, email):
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")


def create_profile(name, email, path=None):
    """Create a new profile and persist it to *path* (default: profile.json)."""
    _validate(name, email)
    profile = {"name": name, "email": email}
    _save(profile, path or _DEFAULT_PROFILE_PATH)
    return profile


def load_profile(path=None):
    """Load a profile from *path* (default: profile.json).

    Raises FileNotFoundError if the file does not exist.
    """
    resolved = path or _DEFAULT_PROFILE_PATH
    if not os.path.exists(resolved):
        raise FileNotFoundError(f"No profile found at '{resolved}'")
    with open(resolved, encoding="utf-8") as fh:
        return json.load(fh)


def update_profile(data, path=None):
    """Merge *data* into the existing profile and save it.

    If *data* contains an ``email`` key its value is validated before saving.
    """
    if "email" in data and not _EMAIL_RE.match(data["email"]):
        raise ValueError("email must be a valid email address")
    profile = load_profile(path)
    profile.update(data)
    _save(profile, path or _DEFAULT_PROFILE_PATH)
    return profile


def _save(profile, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh, indent=2)
