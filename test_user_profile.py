import json
import os
import tempfile
import pytest

from user_profile import create_profile, load_profile, update_profile


@pytest.fixture()
def profile_path(tmp_path):
    """Return a temporary path for a profile JSON file."""
    return str(tmp_path / "profile.json")


# ---------------------------------------------------------------------------
# create_profile
# ---------------------------------------------------------------------------

class TestCreateProfile:
    def test_creates_profile_file(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        assert os.path.exists(profile_path)

    def test_returns_profile_dict(self, profile_path):
        result = create_profile("Alice", "alice@example.com", profile_path)
        assert result == {"name": "Alice", "email": "alice@example.com"}

    def test_file_contains_correct_json(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        with open(profile_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert data == {"name": "Alice", "email": "alice@example.com"}

    def test_raises_value_error_for_empty_name(self, profile_path):
        with pytest.raises(ValueError, match="name must not be empty"):
            create_profile("", "alice@example.com", profile_path)

    def test_raises_value_error_for_invalid_email(self, profile_path):
        with pytest.raises(ValueError, match="email must be a valid email address"):
            create_profile("Alice", "@bad", profile_path)

    def test_raises_value_error_for_email_without_at(self, profile_path):
        with pytest.raises(ValueError, match="email must be a valid email address"):
            create_profile("Alice", "notanemail", profile_path)


# ---------------------------------------------------------------------------
# load_profile
# ---------------------------------------------------------------------------

class TestLoadProfile:
    def test_loads_existing_profile(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        data = load_profile(profile_path)
        assert data == {"name": "Alice", "email": "alice@example.com"}

    def test_raises_file_not_found_for_missing_path(self, tmp_path):
        nonexistent = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            load_profile(nonexistent)


# ---------------------------------------------------------------------------
# update_profile
# ---------------------------------------------------------------------------

class TestUpdateProfile:
    def test_updates_name(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        result = update_profile({"name": "Alice Smith"}, profile_path)
        assert result["name"] == "Alice Smith"
        assert result["email"] == "alice@example.com"

    def test_updates_are_persisted(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        update_profile({"name": "Alice Smith"}, profile_path)
        data = load_profile(profile_path)
        assert data == {"name": "Alice Smith", "email": "alice@example.com"}

    def test_raises_file_not_found_when_no_profile(self, tmp_path):
        nonexistent = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            update_profile({"name": "Alice"}, nonexistent)

    def test_raises_value_error_for_empty_name_update(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        with pytest.raises(ValueError, match="name must not be empty"):
            update_profile({"name": ""}, profile_path)

    def test_raises_value_error_for_invalid_email_update(self, profile_path):
        create_profile("Alice", "alice@example.com", profile_path)
        with pytest.raises(ValueError, match="email must be a valid email address"):
            update_profile({"email": "@bad"}, profile_path)
