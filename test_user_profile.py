#!/usr/bin/env python3
"""Tests for the user profile module."""

import pytest

from user_profile import (
    ProfileNotFoundError,
    UserProfile,
    UserProfileStore,
    ValidationError,
)


# ---------------------------------------------------------------------------
# UserProfile
# ---------------------------------------------------------------------------

class TestUserProfile:
    def test_attributes_are_stored(self):
        profile = UserProfile("u1", "Alice")
        assert profile.user_id == "u1"
        assert profile.display_name == "Alice"
        assert profile.bio == ""
        assert profile.avatar_url == ""

    def test_optional_fields(self):
        profile = UserProfile("u1", "Alice", bio="Hi", avatar_url="https://example.com/a.png")
        assert profile.bio == "Hi"
        assert profile.avatar_url == "https://example.com/a.png"

    def test_repr_includes_user_id_and_display_name(self):
        profile = UserProfile("u1", "Alice")
        r = repr(profile)
        assert "u1" in r
        assert "Alice" in r


# ---------------------------------------------------------------------------
# UserProfileStore.create_profile – happy path
# ---------------------------------------------------------------------------

class TestCreateProfile:
    def setup_method(self):
        self.store = UserProfileStore()

    def test_create_returns_profile(self):
        profile = self.store.create_profile("u1", "Alice")
        assert isinstance(profile, UserProfile)

    def test_create_stores_profile(self):
        self.store.create_profile("u1", "Alice")
        assert len(self.store) == 1

    def test_display_name_is_stripped(self):
        profile = self.store.create_profile("u1", "  Alice  ")
        assert profile.display_name == "Alice"

    def test_optional_bio_and_avatar(self):
        profile = self.store.create_profile(
            "u1", "Alice", bio="Hello", avatar_url="https://img.example.com/a.png"
        )
        assert profile.bio == "Hello"
        assert profile.avatar_url == "https://img.example.com/a.png"

    def test_multiple_profiles(self):
        self.store.create_profile("u1", "Alice")
        self.store.create_profile("u2", "Bob")
        assert len(self.store) == 2


# ---------------------------------------------------------------------------
# UserProfileStore.create_profile – validation errors
# ---------------------------------------------------------------------------

class TestCreateProfileValidation:
    def setup_method(self):
        self.store = UserProfileStore()

    def test_empty_user_id_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("", "Alice")

    def test_whitespace_user_id_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("   ", "Alice")

    def test_empty_display_name_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "")

    def test_whitespace_display_name_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "   ")

    def test_display_name_too_long_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "A" * 101)

    def test_bio_too_long_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "Alice", bio="x" * 501)

    def test_avatar_url_not_http_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "Alice", avatar_url="ftp://bad.url/img.png")

    def test_avatar_url_too_long_raises(self):
        with pytest.raises(ValidationError):
            self.store.create_profile("u1", "Alice", avatar_url="https://x.com/" + "a" * 2040)

    def test_valid_http_avatar_url_accepted(self):
        profile = self.store.create_profile("u1", "Alice", avatar_url="http://img.example.com/a.png")
        assert profile.avatar_url == "http://img.example.com/a.png"


# ---------------------------------------------------------------------------
# UserProfileStore.get_profile
# ---------------------------------------------------------------------------

class TestGetProfile:
    def setup_method(self):
        self.store = UserProfileStore()

    def test_get_returns_created_profile(self):
        self.store.create_profile("u1", "Alice")
        profile = self.store.get_profile("u1")
        assert profile.user_id == "u1"
        assert profile.display_name == "Alice"

    def test_get_unknown_user_raises_profile_not_found(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.get_profile("nobody")

    def test_get_after_delete_raises_profile_not_found(self):
        self.store.create_profile("u1", "Alice")
        self.store.delete_profile("u1")
        with pytest.raises(ProfileNotFoundError):
            self.store.get_profile("u1")


# ---------------------------------------------------------------------------
# UserProfileStore.update_profile
# ---------------------------------------------------------------------------

class TestUpdateProfile:
    def setup_method(self):
        self.store = UserProfileStore()
        self.store.create_profile("u1", "Alice", bio="Original bio")

    def test_update_display_name(self):
        profile = self.store.update_profile("u1", display_name="Alicia")
        assert profile.display_name == "Alicia"

    def test_update_display_name_is_stripped(self):
        profile = self.store.update_profile("u1", display_name="  Alicia  ")
        assert profile.display_name == "Alicia"

    def test_update_bio(self):
        profile = self.store.update_profile("u1", bio="New bio")
        assert profile.bio == "New bio"

    def test_update_avatar_url(self):
        profile = self.store.update_profile("u1", avatar_url="https://img.example.com/new.png")
        assert profile.avatar_url == "https://img.example.com/new.png"

    def test_update_none_fields_unchanged(self):
        profile = self.store.update_profile("u1")
        assert profile.display_name == "Alice"
        assert profile.bio == "Original bio"

    def test_update_partial_fields(self):
        profile = self.store.update_profile("u1", bio="Updated bio")
        assert profile.display_name == "Alice"
        assert profile.bio == "Updated bio"

    def test_update_unknown_user_raises_profile_not_found(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.update_profile("nobody", display_name="X")

    def test_update_invalid_display_name_raises(self):
        with pytest.raises(ValidationError):
            self.store.update_profile("u1", display_name="")

    def test_update_invalid_bio_raises(self):
        with pytest.raises(ValidationError):
            self.store.update_profile("u1", bio="x" * 501)

    def test_update_invalid_avatar_url_raises(self):
        with pytest.raises(ValidationError):
            self.store.update_profile("u1", avatar_url="not-a-url")


# ---------------------------------------------------------------------------
# UserProfileStore.delete_profile
# ---------------------------------------------------------------------------

class TestDeleteProfile:
    def setup_method(self):
        self.store = UserProfileStore()

    def test_delete_removes_profile(self):
        self.store.create_profile("u1", "Alice")
        self.store.delete_profile("u1")
        assert len(self.store) == 0

    def test_delete_unknown_user_raises_profile_not_found(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.delete_profile("nobody")

    def test_delete_only_targeted_profile(self):
        self.store.create_profile("u1", "Alice")
        self.store.create_profile("u2", "Bob")
        self.store.delete_profile("u1")
        assert len(self.store) == 1
        with pytest.raises(ProfileNotFoundError):
            self.store.get_profile("u1")
        assert self.store.get_profile("u2").display_name == "Bob"
