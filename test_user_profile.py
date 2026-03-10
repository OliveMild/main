import pytest

from user_profile import create_profile, load_profile, update_profile


@pytest.fixture
def profile_path(tmp_path):
    return str(tmp_path / "profile.json")


def test_create_and_load_profile(profile_path):
    create_profile("Alice", "alice@example.com", profile_path)
    profile = load_profile(profile_path)
    assert profile == {"name": "Alice", "email": "alice@example.com"}


def test_update_profile(profile_path):
    create_profile("Alice", "alice@example.com", profile_path)
    update_profile({"name": "Alice Smith"}, profile_path)
    profile = load_profile(profile_path)
    assert profile["name"] == "Alice Smith"
    assert profile["email"] == "alice@example.com"


def test_load_profile_nonexistent_raises():
    with pytest.raises(FileNotFoundError):
        load_profile("/nonexistent/profile.json")


def test_create_profile_empty_name_raises(profile_path):
    with pytest.raises(ValueError, match="name must not be empty"):
        create_profile("", "alice@example.com", profile_path)


def test_create_profile_invalid_email_raises(profile_path):
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "@bad", profile_path)
