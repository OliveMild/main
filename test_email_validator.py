"""Tests for the email_validator module."""

import pytest
from email_validator import InvalidEmailError, is_valid_email, validate_email


class TestIsValidEmail:
    def test_standard_address(self):
        assert is_valid_email("user@example.com") is True

    def test_plus_tag_and_subdomain(self):
        assert is_valid_email("user+tag@mail.example.co.uk") is True

    def test_none_returns_false(self):
        assert is_valid_email(None) is False

    def test_integer_returns_false(self):
        assert is_valid_email(42) is False

    def test_empty_string_returns_false(self):
        assert is_valid_email("") is False

    def test_missing_at_sign(self):
        assert is_valid_email("userexample.com") is False

    def test_double_at_sign(self):
        assert is_valid_email("bad@@addr") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_consecutive_dots_in_local_returns_false(self):
        assert is_valid_email("user..name@example.com") is False

    def test_leading_dot_in_local_returns_false(self):
        assert is_valid_email(".user@example.com") is False

    def test_trailing_dot_in_local_returns_false(self):
        assert is_valid_email("user.@example.com") is False


class TestValidateEmail:
    def test_valid_address_is_returned(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_invalid_address_raises(self):
        with pytest.raises(InvalidEmailError, match="Invalid email address: 'bad@@addr'"):
            validate_email("bad@@addr")

    def test_none_raises(self):
        with pytest.raises(InvalidEmailError):
            validate_email(None)

    def test_invalid_email_error_is_value_error(self):
        with pytest.raises(ValueError):
            validate_email("not-an-email")
