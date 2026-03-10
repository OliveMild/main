#!/usr/bin/env python3
"""Tests for user_profile module."""

import pytest
from user_profile import (
    InvalidFieldError,
    MissingFieldError,
    UserProfile,
    UserProfileError,
)


class TestUserProfileCreation:
    def test_valid_profile(self):
        profile = UserProfile(username="alice", email="alice@example.com")
        assert profile.username == "alice"
        assert profile.email == "alice@example.com"
        assert profile.display_name == "alice"
        assert profile.bio == ""

    def test_valid_profile_with_optional_fields(self):
        profile = UserProfile(
            username="bob",
            email="bob@example.com",
            display_name="Bob Smith",
            bio="A developer",
        )
        assert profile.display_name == "Bob Smith"
        assert profile.bio == "A developer"

    def test_missing_username_raises(self):
        with pytest.raises(MissingFieldError) as exc_info:
            UserProfile(username="", email="user@example.com")
        assert "username" in str(exc_info.value)

    def test_missing_email_raises(self):
        with pytest.raises(MissingFieldError) as exc_info:
            UserProfile(username="alice", email="")
        assert "email" in str(exc_info.value)

    def test_username_too_short_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="ab", email="user@example.com")

    def test_username_too_long_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="a" * 51, email="user@example.com")

    def test_username_invalid_characters_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="user name!", email="user@example.com")

    def test_username_with_hyphens_and_underscores(self):
        profile = UserProfile(username="user-name_1", email="user@example.com")
        assert profile.username == "user-name_1"

    def test_email_missing_at_sign_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="alice", email="invalidemail.com")

    def test_email_multiple_at_signs_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="alice", email="a@b@example.com")

    def test_email_empty_local_part_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="alice", email="@example.com")

    def test_email_domain_without_dot_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="alice", email="alice@nodot")

    def test_email_with_whitespace_raises(self):
        with pytest.raises(InvalidFieldError):
            UserProfile(username="alice", email=" alice@example.com")

    def test_error_is_subclass_of_user_profile_error(self):
        with pytest.raises(UserProfileError):
            UserProfile(username="", email="user@example.com")


class TestUserProfileUpdate:
    def setup_method(self):
        self.profile = UserProfile(username="alice", email="alice@example.com")

    def test_update_email(self):
        self.profile.update(email="newalice@example.com")
        assert self.profile.email == "newalice@example.com"

    def test_update_display_name(self):
        self.profile.update(display_name="Alice W.")
        assert self.profile.display_name == "Alice W."

    def test_update_bio(self):
        self.profile.update(bio="Updated bio")
        assert self.profile.bio == "Updated bio"

    def test_update_invalid_email_raises(self):
        with pytest.raises(InvalidFieldError):
            self.profile.update(email="bademail")

    def test_update_disallowed_field_raises(self):
        with pytest.raises(InvalidFieldError):
            self.profile.update(username="newname")

    def test_update_display_name_non_string_raises(self):
        with pytest.raises(InvalidFieldError):
            self.profile.update(display_name=123)

    def test_update_bio_non_string_raises(self):
        with pytest.raises(InvalidFieldError):
            self.profile.update(bio=None)

    def test_update_multiple_fields(self):
        self.profile.update(display_name="Alice W.", bio="New bio")
        assert self.profile.display_name == "Alice W."
        assert self.profile.bio == "New bio"


class TestUserProfileToDict:
    def test_to_dict(self):
        profile = UserProfile(
            username="alice",
            email="alice@example.com",
            display_name="Alice",
            bio="Hello",
        )
        result = profile.to_dict()
        assert result == {
            "username": "alice",
            "email": "alice@example.com",
            "display_name": "Alice",
            "bio": "Hello",
        }


class TestUserProfileRepr:
    def test_repr(self):
        profile = UserProfile(username="alice", email="alice@example.com")
        assert "alice" in repr(profile)
        assert "alice@example.com" in repr(profile)
