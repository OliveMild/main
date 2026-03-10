import json
import os
import re

DEFAULT_PROFILE_PATH = "profile.json"


def _validate_name(name: str) -> None:
    if not name:
        raise ValueError("name must not be empty")


def _validate_email(email: str) -> None:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValueError("email must be a valid email address")


def create_profile(name: str, email: str, path: str = DEFAULT_PROFILE_PATH) -> dict:
    _validate_name(name)
    _validate_email(email)
    profile = {"name": name, "email": email}
    with open(path, "w") as f:
        json.dump(profile, f)
    return profile


def load_profile(path: str = DEFAULT_PROFILE_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Profile not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def update_profile(data: dict, path: str = DEFAULT_PROFILE_PATH) -> dict:
    if "name" in data:
        _validate_name(data["name"])
    if "email" in data:
        _validate_email(data["email"])
    profile = load_profile(path)
    profile.update(data)
    with open(path, "w") as f:
        json.dump(profile, f)
    return profile
