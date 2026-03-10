import json
import os
import pytest

from user_profile import create_profile, load_profile, update_profile


@pytest.fixture(autouse=True)
def tmp_profile(tmp_path, monkeypatch):
    """Redirect the default profile path to a temporary directory."""
    import user_profile as _up
    profile_file = str(tmp_path / "profile.json")
    monkeypatch.setattr(_up, "_DEFAULT_PROFILE_PATH", profile_file)
    return profile_file


# ---------------------------------------------------------------------------
# create_profile
# ---------------------------------------------------------------------------

def test_create_profile_saves_file(tmp_profile):
    create_profile("Alice", "alice@example.com")
    with open(tmp_profile, encoding="utf-8") as fh:
        data = json.load(fh)
    assert data == {"name": "Alice", "email": "alice@example.com"}


def test_create_profile_returns_dict():
    profile = create_profile("Bob", "bob@example.com")
    assert profile == {"name": "Bob", "email": "bob@example.com"}


def test_create_profile_empty_name_raises():
    with pytest.raises(ValueError, match="name must not be empty"):
        create_profile("", "alice@example.com")


def test_create_profile_invalid_email_raises():
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "@bad")


def test_create_profile_invalid_email_no_domain():
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "alice@")


def test_create_profile_invalid_email_no_at():
    with pytest.raises(ValueError, match="email must be a valid email address"):
        create_profile("Alice", "aliceexample.com")


# ---------------------------------------------------------------------------
# load_profile
# ---------------------------------------------------------------------------

def test_load_profile_returns_data():
    create_profile("Alice", "alice@example.com")
    profile = load_profile()
    assert profile == {"name": "Alice", "email": "alice@example.com"}


def test_load_profile_nonexistent_raises():
    with pytest.raises(FileNotFoundError):
        load_profile("/nonexistent/profile.json")


def test_load_profile_default_path_raises_when_missing():
    # tmp_profile fixture redirects default path to a fresh tmp dir,
    # so no profile.json exists yet.
    with pytest.raises(FileNotFoundError):
        load_profile()


# ---------------------------------------------------------------------------
# update_profile
# ---------------------------------------------------------------------------

def test_update_profile_merges_data():
    create_profile("Alice", "alice@example.com")
    update_profile({"name": "Alice Smith"})
    profile = load_profile()
    assert profile == {"name": "Alice Smith", "email": "alice@example.com"}


def test_update_profile_returns_updated():
    create_profile("Alice", "alice@example.com")
    result = update_profile({"email": "new@example.com"})
    assert result["email"] == "new@example.com"
    assert result["name"] == "Alice"


def test_update_profile_invalid_email_raises():
    create_profile("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="email must be a valid email address"):
        update_profile({"email": "@bad"})
