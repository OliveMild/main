import os
import json
import pytest

from user_profile import create_profile, load_profile, update_profile


@pytest.fixture
def profile_path(tmp_path):
    return str(tmp_path / "profile.json")


def test_create_and_load(profile_path):
    create_profile("Alice", "alice@example.com", profile_path)
    result = load_profile(profile_path)
    assert result == {"name": "Alice", "email": "alice@example.com"}


def test_update_profile(profile_path):
    create_profile("Alice", "alice@example.com", profile_path)
    update_profile({"name": "Alice Smith"}, profile_path)
    result = load_profile(profile_path)
    assert result["name"] == "Alice Smith"
    assert result["email"] == "alice@example.com"


def test_load_nonexistent_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_profile("/nonexistent/path/to/profile.json")


def test_create_empty_name_raises_value_error(profile_path):
    with pytest.raises(ValueError, match="name must not be empty"):
        create_profile("", "alice@example.com", profile_path)


def test_create_invalid_email_raises_value_error(profile_path):
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "@bad", profile_path)


def test_create_invalid_email_no_tld(profile_path):
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "alice@nodot", profile_path)


def test_update_invalid_email_raises_value_error(profile_path):
    create_profile("Alice", "alice@example.com", profile_path)
    with pytest.raises(ValueError, match="email must be a valid email address"):
        update_profile({"email": "@bad"}, profile_path)


def test_update_nonexistent_profile_raises():
    with pytest.raises(FileNotFoundError):
        update_profile({"name": "Bob"}, "/nonexistent/path/profile.json")
