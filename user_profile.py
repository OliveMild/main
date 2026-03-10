import json
import re

_DEFAULT_PROFILE_PATH = "profile.json"
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")


def create_profile(name: str, email: str, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Create a new profile and persist it to *path* (JSON).

    Raises:
        ValueError: if *name* is empty or *email* is not a valid email address.
    """
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")

    profile = {"name": name, "email": email}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh, indent=2)


def load_profile(path: str = _DEFAULT_PROFILE_PATH) -> dict:
    """Load and return the profile stored at *path*.

    Raises:
        FileNotFoundError: if *path* does not exist.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Profile not found: {path}") from e


def update_profile(data: dict, path: str = _DEFAULT_PROFILE_PATH) -> None:
    """Merge *data* into the existing profile stored at *path*.

    Raises:
        FileNotFoundError: if *path* does not exist.
    """
    profile = load_profile(path)
    profile.update(data)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(profile, fh, indent=2)
