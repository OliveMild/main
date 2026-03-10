#!/usr/bin/env python3
"""Tests for profile creation validation."""

import pytest
from profile import create_profile, validate_profile, ProfileValidationError


# ---------------------------------------------------------------------------
# Helper: a valid base profile that all tests can start from
# ---------------------------------------------------------------------------
VALID_DATA = {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "age": 30,
    "username": "jane_doe",
}


def valid(**overrides):
    """Return a copy of VALID_DATA with optional field overrides."""
    return {**VALID_DATA, **overrides}


# ---------------------------------------------------------------------------
# create_profile – happy path
# ---------------------------------------------------------------------------
class TestCreateProfileSuccess:
    def test_returns_profile_dict(self):
        profile = create_profile(VALID_DATA)
        assert profile["name"] == "Jane Doe"
        assert profile["email"] == "jane.doe@example.com"
        assert profile["age"] == 30
        assert profile["username"] == "jane_doe"

    def test_email_normalized_to_lowercase(self):
        profile = create_profile(valid(email="Jane.Doe@Example.COM"))
        assert profile["email"] == "jane.doe@example.com"

    def test_name_strips_surrounding_whitespace(self):
        profile = create_profile(valid(name="  Alice  "))
        assert profile["name"] == "Alice"

    def test_name_with_hyphen(self):
        profile = create_profile(valid(name="Mary-Jane"))
        assert profile["name"] == "Mary-Jane"

    def test_name_with_apostrophe(self):
        profile = create_profile(valid(name="O'Brien"))
        assert profile["name"] == "O'Brien"

    def test_minimum_age_zero(self):
        profile = create_profile(valid(age=0))
        assert profile["age"] == 0

    def test_maximum_age_150(self):
        profile = create_profile(valid(age=150))
        assert profile["age"] == 150

    def test_username_with_numbers(self):
        profile = create_profile(valid(username="user123"))
        assert profile["username"] == "user123"

    def test_username_minimum_length(self):
        profile = create_profile(valid(username="abc"))
        assert profile["username"] == "abc"

    def test_username_maximum_length(self):
        profile = create_profile(valid(username="a" * 30))
        assert profile["username"] == "a" * 30


# ---------------------------------------------------------------------------
# Missing / None required fields
# ---------------------------------------------------------------------------
class TestMissingRequiredFields:
    @pytest.mark.parametrize("field", ["name", "email", "age", "username"])
    def test_missing_field_raises(self, field):
        data = {k: v for k, v in VALID_DATA.items() if k != field}
        with pytest.raises(ProfileValidationError, match=f"'{field}' is required"):
            create_profile(data)

    @pytest.mark.parametrize("field", ["name", "email", "age", "username"])
    def test_none_field_raises(self, field):
        with pytest.raises(ProfileValidationError, match=f"'{field}' is required"):
            create_profile(valid(**{field: None}))


# ---------------------------------------------------------------------------
# Name validation
# ---------------------------------------------------------------------------
class TestNameValidation:
    def test_empty_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name=""))

    def test_whitespace_only_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name="   "))

    def test_non_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name=42))

    def test_too_long_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name="A" * 101))

    def test_name_with_digits_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name="Jane123"))

    def test_name_with_special_chars_raises(self):
        with pytest.raises(ProfileValidationError, match="'name'"):
            create_profile(valid(name="Jane@Doe"))


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------
class TestEmailValidation:
    def test_missing_at_sign_raises(self):
        with pytest.raises(ProfileValidationError, match="'email'"):
            create_profile(valid(email="janedoeexample.com"))

    def test_missing_domain_raises(self):
        with pytest.raises(ProfileValidationError, match="'email'"):
            create_profile(valid(email="jane@"))

    def test_missing_tld_raises(self):
        with pytest.raises(ProfileValidationError, match="'email'"):
            create_profile(valid(email="jane@example"))

    def test_empty_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'email'"):
            create_profile(valid(email=""))

    def test_non_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'email'"):
            create_profile(valid(email=123))

    def test_valid_plus_addressing(self):
        profile = create_profile(valid(email="jane+tag@example.com"))
        assert "jane+tag@example.com" in profile["email"]


# ---------------------------------------------------------------------------
# Age validation
# ---------------------------------------------------------------------------
class TestAgeValidation:
    def test_negative_age_raises(self):
        with pytest.raises(ProfileValidationError, match="'age'"):
            create_profile(valid(age=-1))

    def test_age_above_150_raises(self):
        with pytest.raises(ProfileValidationError, match="'age'"):
            create_profile(valid(age=151))

    def test_float_age_raises(self):
        with pytest.raises(ProfileValidationError, match="'age'"):
            create_profile(valid(age=25.5))

    def test_string_age_raises(self):
        with pytest.raises(ProfileValidationError, match="'age'"):
            create_profile(valid(age="25"))

    def test_bool_age_raises(self):
        with pytest.raises(ProfileValidationError, match="'age'"):
            create_profile(valid(age=True))


# ---------------------------------------------------------------------------
# Username validation
# ---------------------------------------------------------------------------
class TestUsernameValidation:
    def test_too_short_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username="ab"))

    def test_too_long_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username="a" * 31))

    def test_empty_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username=""))

    def test_special_chars_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username="jane-doe"))

    def test_spaces_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username="jane doe"))

    def test_non_string_raises(self):
        with pytest.raises(ProfileValidationError, match="'username'"):
            create_profile(valid(username=12345))
