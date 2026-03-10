#!/usr/bin/env python3
"""Tests for the user profile module."""

import pytest

from user_profile import (
    ProfileManager,
    UserProfile,
    ValidationError,
)


# ---------------------------------------------------------------------------
# UserProfile.__init__ – validation
# ---------------------------------------------------------------------------

class TestUserProfileInit:
    def test_empty_username_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("", "Alice")

    def test_whitespace_username_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("   ", "Alice")

    def test_too_long_username_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("a" * 51, "Alice")

    def test_username_with_leading_whitespace_raises(self):
        with pytest.raises(ValidationError):
            UserProfile(" alice", "Alice")

    def test_valid_profile_created(self):
        p = UserProfile("alice", "Alice", "Bio", "https://example.com/a.png")
        assert p.username == "alice"
        assert p.display_name == "Alice"
        assert p.bio == "Bio"
        assert p.avatar_url == "https://example.com/a.png"

    def test_defaults_are_empty_strings(self):
        p = UserProfile("alice", "Alice")
        assert p.bio == ""
        assert p.avatar_url == ""

    def test_empty_display_name_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "")

    def test_whitespace_display_name_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "   ")

    def test_too_long_display_name_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "a" * 101)

    def test_too_long_bio_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "Alice", "x" * 501)

    def test_invalid_avatar_url_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "Alice", "", "not-a-url")

    def test_valid_avatar_url_https(self):
        p = UserProfile("alice", "Alice", "", "https://example.com/avatar.png")
        assert p.avatar_url == "https://example.com/avatar.png"

    def test_valid_avatar_url_http(self):
        p = UserProfile("alice", "Alice", "", "http://example.com/avatar.jpg")
        assert p.avatar_url == "http://example.com/avatar.jpg"

    def test_invalid_avatar_url_ftp_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("alice", "Alice", "", "ftp://example.com/avatar.png")

    def test_avatar_url_with_port(self):
        p = UserProfile(
            "alice", "Alice", "", "https://example.com:8080/avatar.png"
        )
        assert p.avatar_url == "https://example.com:8080/avatar.png"

    def test_max_display_name_passes(self):
        p = UserProfile("alice", "a" * 100)
        assert len(p.display_name) == 100

    def test_max_bio_passes(self):
        p = UserProfile("alice", "Alice", "x" * 500)
        assert len(p.bio) == 500


# ---------------------------------------------------------------------------
# UserProfile.update
# ---------------------------------------------------------------------------

class TestUserProfileUpdate:
    def _make_profile(self) -> UserProfile:
        return UserProfile("alice", "Alice", "Hello!", "https://example.com/a.png")

    def test_update_display_name(self):
        p = self._make_profile()
        p.update(display_name="Alicia")
        assert p.display_name == "Alicia"

    def test_update_bio(self):
        p = self._make_profile()
        p.update(bio="New bio")
        assert p.bio == "New bio"

    def test_update_avatar_url(self):
        p = self._make_profile()
        p.update(avatar_url="https://example.com/new.png")
        assert p.avatar_url == "https://example.com/new.png"

    def test_partial_update_preserves_other_fields(self):
        p = self._make_profile()
        p.update(display_name="Alicia")
        assert p.bio == "Hello!"
        assert p.avatar_url == "https://example.com/a.png"

    def test_update_with_invalid_display_name_raises(self):
        p = self._make_profile()
        with pytest.raises(ValidationError):
            p.update(display_name="")

    def test_update_with_invalid_bio_raises(self):
        p = self._make_profile()
        with pytest.raises(ValidationError):
            p.update(bio="x" * 501)

    def test_update_with_invalid_avatar_url_raises(self):
        p = self._make_profile()
        with pytest.raises(ValidationError):
            p.update(avatar_url="not-a-url")

    def test_failed_update_leaves_profile_unchanged(self):
        p = self._make_profile()
        try:
            p.update(display_name="", bio="changed bio")
        except ValidationError:
            pass
        assert p.display_name == "Alice"
        assert p.bio == "Hello!"


# ---------------------------------------------------------------------------
# ProfileManager.create_profile – happy path
# ---------------------------------------------------------------------------

class TestProfileManagerCreate:
    def setup_method(self):
        self.manager = ProfileManager()

    def test_create_returns_profile(self):
        profile = self.manager.create_profile("alice", "Alice")
        assert isinstance(profile, UserProfile)

    def test_created_profile_attributes(self):
        profile = self.manager.create_profile(
            "alice", "Alice", "Bio", "https://example.com/a.png"
        )
        assert profile.username == "alice"
        assert profile.display_name == "Alice"
        assert profile.bio == "Bio"
        assert profile.avatar_url == "https://example.com/a.png"

    def test_manager_length_increases(self):
        assert len(self.manager) == 0
        self.manager.create_profile("alice", "Alice")
        assert len(self.manager) == 1
        self.manager.create_profile("bob", "Bob")
        assert len(self.manager) == 2

    def test_get_profile_returns_profile(self):
        self.manager.create_profile("alice", "Alice")
        p = self.manager.get_profile("alice")
        assert p is not None
        assert p.username == "alice"

    def test_get_profile_case_insensitive(self):
        self.manager.create_profile("alice", "Alice")
        assert self.manager.get_profile("ALICE") is not None

    def test_get_profile_unknown_returns_none(self):
        assert self.manager.get_profile("nobody") is None


# ---------------------------------------------------------------------------
# ProfileManager – duplicate detection
# ---------------------------------------------------------------------------

class TestProfileManagerDuplicates:
    def setup_method(self):
        self.manager = ProfileManager()
        self.manager.create_profile("alice", "Alice")

    def test_duplicate_username_raises(self):
        with pytest.raises(ValueError):
            self.manager.create_profile("alice", "Alice 2")

    def test_duplicate_username_case_insensitive(self):
        with pytest.raises(ValueError):
            self.manager.create_profile("ALICE", "Alice 2")


# ---------------------------------------------------------------------------
# ProfileManager – validation on create
# ---------------------------------------------------------------------------

class TestProfileManagerValidation:
    def setup_method(self):
        self.manager = ProfileManager()

    def test_empty_display_name_raises(self):
        with pytest.raises(ValidationError):
            self.manager.create_profile("alice", "")

    def test_too_long_bio_raises(self):
        with pytest.raises(ValidationError):
            self.manager.create_profile("alice", "Alice", "x" * 501)

    def test_invalid_avatar_url_raises(self):
        with pytest.raises(ValidationError):
            self.manager.create_profile("alice", "Alice", "", "not-a-url")


# ---------------------------------------------------------------------------
# ProfileManager.delete_profile
# ---------------------------------------------------------------------------

class TestProfileManagerDelete:
    def setup_method(self):
        self.manager = ProfileManager()
        self.manager.create_profile("alice", "Alice")

    def test_delete_existing_returns_true(self):
        assert self.manager.delete_profile("alice") is True

    def test_delete_reduces_length(self):
        self.manager.delete_profile("alice")
        assert len(self.manager) == 0

    def test_delete_nonexistent_returns_false(self):
        assert self.manager.delete_profile("nobody") is False

    def test_get_profile_after_delete_returns_none(self):
        self.manager.delete_profile("alice")
        assert self.manager.get_profile("alice") is None

    def test_delete_case_insensitive(self):
        assert self.manager.delete_profile("ALICE") is True
