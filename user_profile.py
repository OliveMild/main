import json
import os
import re

_DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate(name, email):
    if not name:
        raise ValueError("name must not be empty")
    if not _EMAIL_REGEX.match(email):
        raise ValueError("email must be a valid email address")


def create_profile(name, email, path=None):
    _validate(name, email)
    profile = {"name": name, "email": email}
    target = path or _DEFAULT_PROFILE_PATH
    with open(target, "w", encoding="utf-8") as f:
        json.dump(profile, f)
    return profile


def load_profile(path=None):
    target = path or _DEFAULT_PROFILE_PATH
    if not os.path.exists(target):
        raise FileNotFoundError(f"No profile found at {target!r}")
    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)


def update_profile(updates, path=None):
    target = path or _DEFAULT_PROFILE_PATH
    profile = load_profile(target)
    merged = {**profile, **updates}
    _validate(merged["name"], merged["email"])
    with open(target, "w", encoding="utf-8") as f:
        json.dump(merged, f)
    return merged
