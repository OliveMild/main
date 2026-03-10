import json
import os
import re

PROFILE_FILE = "profile_data.json"

_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$"
)


def _validate_email(email):
    """Return True if *email* looks like a valid e-mail address."""
    return bool(_EMAIL_RE.match(email))


def create_profile(name, email, path=None):
    """Create a user profile and persist it to *path* (default: PROFILE_FILE).

    Raises:
        ValueError: if *name* is empty or *email* is not a valid address.
    """
    if not name:
        raise ValueError("name must not be empty")
    if not _validate_email(email):
        raise ValueError("email must be a valid email address")

    profile = {"name": name, "email": email}
    dest = path if path is not None else PROFILE_FILE
    with open(dest, "w") as f:
        json.dump(profile, f, indent=2)
    return profile


def load_profile(path=None):
    """Load and return the user profile from *path* (default: PROFILE_FILE).

    Raises:
        FileNotFoundError: if the profile file does not exist.
    """
    src = path if path is not None else PROFILE_FILE
    if not os.path.exists(src):
        raise FileNotFoundError(f"Profile file not found: {src}")
    with open(src, "r") as f:
        return json.load(f)


def update_profile(data, path=None):
    """Update the stored user profile with the key/value pairs in *data*.

    The profile is loaded, merged with *data*, and written back.

    Raises:
        FileNotFoundError: if the profile file does not exist.
        ValueError: if *data* contains an empty *name* or invalid *email*.
    """
    profile = load_profile(path)
    if "name" in data and not data["name"]:
        raise ValueError("name must not be empty")
    if "email" in data and not _validate_email(data["email"]):
        raise ValueError("email must be a valid email address")
    profile.update(data)
    dest = path if path is not None else PROFILE_FILE
    with open(dest, "w") as f:
        json.dump(profile, f, indent=2)
    return profile
