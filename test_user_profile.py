import json
import os

import pytest

from user_profile import create_profile, load_profile, update_profile


@pytest.fixture
def profile_path(tmp_path):
    return str(tmp_path / "profile.json")


class TestCreateProfile:
    def test_creates_profile_file(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        assert os.path.exists(profile_path)

    def test_profile_contents(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        with open(profile_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data == {"name": "Alice", "email": "alice@example.com"}

    def test_empty_name_raises(self, profile_path):
        with pytest.raises(ValueError, match="name must not be empty"):
            create_profile("", "alice@example.com", path=profile_path)

    def test_invalid_email_raises(self, profile_path):
        with pytest.raises(ValueError, match="email must be a valid email address"):
            create_profile("Alice", "@bad", path=profile_path)

    def test_missing_at_sign_raises(self, profile_path):
        with pytest.raises(ValueError, match="email must be a valid email address"):
            create_profile("Alice", "notanemail", path=profile_path)

    def test_consecutive_dots_in_domain_raises(self, profile_path):
        with pytest.raises(ValueError, match="email must be a valid email address"):
            create_profile("Alice", "user@domain..com", path=profile_path)


class TestLoadProfile:
    def test_loads_existing_profile(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        data = load_profile(path=profile_path)
        assert data == {"name": "Alice", "email": "alice@example.com"}

    def test_nonexistent_path_raises(self, tmp_path):
        missing = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            load_profile(path=missing)


class TestUpdateProfile:
    def test_updates_name(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        update_profile({"name": "Alice Smith"}, path=profile_path)
        data = load_profile(path=profile_path)
        assert data["name"] == "Alice Smith"
        assert data["email"] == "alice@example.com"

    def test_updates_email(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        update_profile({"email": "alice.smith@example.com"}, path=profile_path)
        data = load_profile(path=profile_path)
        assert data["email"] == "alice.smith@example.com"
        assert data["name"] == "Alice"

    def test_empty_name_in_update_raises(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        with pytest.raises(ValueError, match="name must not be empty"):
            update_profile({"name": ""}, path=profile_path)

    def test_invalid_email_in_update_raises(self, profile_path):
        create_profile("Alice", "alice@example.com", path=profile_path)
        with pytest.raises(ValueError, match="email must be a valid email address"):
            update_profile({"email": "@bad"}, path=profile_path)

    def test_update_nonexistent_profile_raises(self, tmp_path):
        missing = str(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            update_profile({"name": "Bob"}, path=missing)
