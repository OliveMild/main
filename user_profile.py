import json
import re

DEFAULT_PROFILE_PATH = "profile.json"
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate(name: str, email: str) -> None:
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_RE.match(email):
        raise ValueError("email must be a valid email address")


def create_profile(name: str, email: str, path: str = DEFAULT_PROFILE_PATH) -> None:
    _validate(name, email)
    with open(path, "w") as f:
        json.dump({"name": name, "email": email}, f)


def load_profile(path: str = DEFAULT_PROFILE_PATH) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Profile not found at '{path}'")


def update_profile(updates: dict, path: str = DEFAULT_PROFILE_PATH) -> None:
    profile = load_profile(path)
    profile.update(updates)
    _validate(profile.get("name", ""), profile.get("email", ""))
    with open(path, "w") as f:
        json.dump(profile, f)
