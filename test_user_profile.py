import os
import pytest
from user_profile import create_profile, load_profile, update_profile


@pytest.fixture(autouse=True)
def tmp_profile(tmp_path, monkeypatch):
    """Point every test at a fresh temporary profile file."""
    profile_file = str(tmp_path / "profile.json")
    # Monkeypatch the module-level default so helpers called without an
    # explicit path use the temp file rather than the real filesystem.
    import user_profile
    monkeypatch.setattr(user_profile, "_DEFAULT_PROFILE_PATH", profile_file)
    return profile_file


def test_create_and_load(tmp_profile):
    create_profile("Alice", "alice@example.com", path=tmp_profile)
    profile = load_profile(tmp_profile)
    assert profile == {"name": "Alice", "email": "alice@example.com"}


def test_update_profile(tmp_profile):
    create_profile("Alice", "alice@example.com", path=tmp_profile)
    update_profile({"name": "Alice Smith"}, path=tmp_profile)
    profile = load_profile(tmp_profile)
    assert profile["name"] == "Alice Smith"
    assert profile["email"] == "alice@example.com"


def test_load_nonexistent_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_profile(str(tmp_path / "nonexistent.json"))


def test_create_empty_name_raises(tmp_profile):
    with pytest.raises(ValueError, match="name must not be empty"):
        create_profile("", "alice@example.com", path=tmp_profile)


def test_create_invalid_email_raises(tmp_profile):
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "@bad", path=tmp_profile)
