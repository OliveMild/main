import os
import pytest
from user_profile import create_profile, load_profile, update_profile

PROFILE_PATH = "/tmp/test_profile.json"


def teardown_function():
    if os.path.exists(PROFILE_PATH):
        os.remove(PROFILE_PATH)


def test_create_and_load_profile():
    create_profile("Alice", "alice@example.com", PROFILE_PATH)
    profile = load_profile(PROFILE_PATH)
    assert profile == {"name": "Alice", "email": "alice@example.com"}


def test_update_profile():
    create_profile("Alice", "alice@example.com", PROFILE_PATH)
    update_profile({"name": "Alice Smith"}, PROFILE_PATH)
    profile = load_profile(PROFILE_PATH)
    assert profile["name"] == "Alice Smith"
    assert profile["email"] == "alice@example.com"


def test_load_profile_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_profile("/nonexistent/path/profile.json")


def test_create_profile_empty_name():
    with pytest.raises(ValueError, match="name must not be empty"):
        create_profile("", "alice@example.com", PROFILE_PATH)


def test_create_profile_invalid_email():
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "@bad", PROFILE_PATH)


def test_update_profile_invalid_email():
    create_profile("Alice", "alice@example.com", PROFILE_PATH)
    with pytest.raises(ValueError, match="email must be a valid email address"):
        update_profile({"email": "@bad"}, PROFILE_PATH)


def test_update_profile_empty_name():
    create_profile("Alice", "alice@example.com", PROFILE_PATH)
    with pytest.raises(ValueError, match="name must not be empty"):
        update_profile({"name": ""}, PROFILE_PATH)
