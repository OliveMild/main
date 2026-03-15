#!/usr/bin/env python3
"""Tests for the user_profile module."""

import pytest
from user_profile import (
    UserProfile,
    UserProfileError,
    InvalidEmailError,
    InvalidUsernameError,
    InvalidAgeError,
)


# ---------------------------------------------------------------------------
# UserProfile creation – happy path
# ---------------------------------------------------------------------------

class TestUserProfileCreation:
    def test_valid_profile(self):
        profile = UserProfile(username="alice", email="alice@example.com", age=30)
        assert profile.username == "alice"
        assert profile.email == "alice@example.com"
        assert profile.age == 30

    def test_valid_profile_without_age(self):
        profile = UserProfile(username="bob123", email="bob@example.com")
        assert profile.username == "bob123"
        assert profile.email == "bob@example.com"
        assert profile.age is None

    def test_username_with_underscores(self):
        profile = UserProfile(username="john_doe", email="john@example.com")
        assert profile.username == "john_doe"

    def test_username_minimum_length(self):
        profile = UserProfile(username="abc", email="abc@example.com")
        assert profile.username == "abc"

    def test_username_maximum_length(self):
        username = "a" * 30
        profile = UserProfile(username=username, email="user@example.com")
        assert profile.username == username

    def test_age_zero(self):
        profile = UserProfile(username="baby", email="baby@example.com", age=0)
        assert profile.age == 0

    def test_age_maximum(self):
        profile = UserProfile(username="elder", email="elder@example.com", age=150)
        assert profile.age == 150


# ---------------------------------------------------------------------------
# Username validation
# ---------------------------------------------------------------------------

class TestUsernameValidation:
    def test_too_short_username_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username="ab", email="ab@example.com")

    def test_too_long_username_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username="a" * 31, email="user@example.com")

    def test_username_with_space_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username="john doe", email="john@example.com")

    def test_username_with_special_chars_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username="user@name", email="user@example.com")

    def test_empty_username_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username="", email="user@example.com")

    def test_non_string_username_raises(self):
        with pytest.raises(InvalidUsernameError):
            UserProfile(username=123, email="user@example.com")


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------

class TestEmailValidation:
    def test_missing_at_sign_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email="invalidemail.com")

    def test_missing_domain_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email="user@")

    def test_missing_local_part_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email="@example.com")

    def test_empty_email_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email="")

    def test_email_with_spaces_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email="user @example.com")

    def test_non_string_email_raises(self):
        with pytest.raises(InvalidEmailError):
            UserProfile(username="user", email=None)


# ---------------------------------------------------------------------------
# Age validation
# ---------------------------------------------------------------------------

class TestAgeValidation:
    def test_negative_age_raises(self):
        with pytest.raises(InvalidAgeError):
            UserProfile(username="user", email="user@example.com", age=-1)

    def test_age_above_maximum_raises(self):
        with pytest.raises(InvalidAgeError):
            UserProfile(username="user", email="user@example.com", age=151)

    def test_string_age_raises(self):
        with pytest.raises(InvalidAgeError):
            UserProfile(username="user", email="user@example.com", age="30")

    def test_float_age_raises(self):
        with pytest.raises(InvalidAgeError):
            UserProfile(username="user", email="user@example.com", age=25.5)


# ---------------------------------------------------------------------------
# update()
# ---------------------------------------------------------------------------

class TestUpdateMethod:
    def test_update_email(self):
        profile = UserProfile(username="user", email="old@example.com")
        profile.update(email="new@example.com")
        assert profile.email == "new@example.com"

    def test_update_age(self):
        profile = UserProfile(username="user", email="user@example.com")
        profile.update(age=25)
        assert profile.age == 25

    def test_update_username(self):
        profile = UserProfile(username="oldname", email="user@example.com")
        profile.update(username="newname")
        assert profile.username == "newname"

    def test_update_with_invalid_email_raises(self):
        profile = UserProfile(username="user", email="user@example.com")
        with pytest.raises(InvalidEmailError):
            profile.update(email="not-an-email")

    def test_update_unknown_field_raises(self):
        profile = UserProfile(username="user", email="user@example.com")
        with pytest.raises(UserProfileError):
            profile.update(nickname="nick")


# ---------------------------------------------------------------------------
# to_dict()
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_with_age(self):
        profile = UserProfile(username="alice", email="alice@example.com", age=25)
        data = profile.to_dict()
        assert data == {"username": "alice", "email": "alice@example.com", "age": 25}

    def test_to_dict_without_age(self):
        profile = UserProfile(username="alice", email="alice@example.com")
        data = profile.to_dict()
        assert data == {"username": "alice", "email": "alice@example.com", "age": None}


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

class TestExceptionHierarchy:
    def test_invalid_email_is_user_profile_error(self):
        assert issubclass(InvalidEmailError, UserProfileError)

    def test_invalid_username_is_user_profile_error(self):
        assert issubclass(InvalidUsernameError, UserProfileError)

    def test_invalid_age_is_user_profile_error(self):
        assert issubclass(InvalidAgeError, UserProfileError)
