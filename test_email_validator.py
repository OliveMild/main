"""Tests for the email_validator module."""

import pytest

from email_validator import InvalidEmailError, is_valid_email, validate_email


# ---------------------------------------------------------------------------
# is_valid_email
# ---------------------------------------------------------------------------

class TestIsValidEmail:
    def test_simple_valid_email(self):
        assert is_valid_email("user@example.com") is True

    def test_subdomain(self):
        assert is_valid_email("user@mail.example.com") is True

    def test_plus_tag(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_multi_part_tld(self):
        assert is_valid_email("user@example.co.uk") is True

    def test_missing_at_sign(self):
        assert is_valid_email("userexample.com") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_missing_local_part(self):
        assert is_valid_email("@example.com") is False

    def test_double_at_sign(self):
        assert is_valid_email("bad@@addr") is False

    def test_consecutive_dots_in_local(self):
        assert is_valid_email("user..name@example.com") is False

    def test_short_tld(self):
        assert is_valid_email("user@example.c") is False

    def test_none_input(self):
        assert is_valid_email(None) is False

    def test_integer_input(self):
        assert is_valid_email(42) is False

    def test_empty_string(self):
        assert is_valid_email("") is False


# ---------------------------------------------------------------------------
# validate_email
# ---------------------------------------------------------------------------

class TestValidateEmail:
    def test_returns_email_when_valid(self):
        email = "alice@example.com"
        assert validate_email(email) == email

    def test_raises_for_invalid_email(self):
        with pytest.raises(InvalidEmailError):
            validate_email("not-an-email")

    def test_raises_for_none(self):
        with pytest.raises(InvalidEmailError):
            validate_email(None)

    def test_raises_for_non_string(self):
        with pytest.raises(InvalidEmailError):
            validate_email(123)

    def test_error_message_contains_value(self):
        bad = "bad@@addr"
        with pytest.raises(InvalidEmailError, match=repr(bad)):
            validate_email(bad)


# ---------------------------------------------------------------------------
# InvalidEmailError hierarchy
# ---------------------------------------------------------------------------

class TestInvalidEmailError:
    def test_is_value_error_subclass(self):
        assert issubclass(InvalidEmailError, ValueError)

    def test_can_be_caught_as_value_error(self):
        with pytest.raises(ValueError):
            validate_email("not-valid")
