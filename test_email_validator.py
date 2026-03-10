#!/usr/bin/env python3
"""Tests for email_validator module."""

import pytest

from email_validator import InvalidEmailError, is_valid_email, validate_email


class TestIsValidEmail:
    """Tests for is_valid_email()."""

    # --- valid addresses ---
    def test_simple_valid(self):
        assert is_valid_email("user@example.com") is True

    def test_subdomain(self):
        assert is_valid_email("user@mail.example.com") is True

    def test_plus_tag(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_dots_in_local(self):
        assert is_valid_email("first.last@example.com") is True

    def test_numeric_local(self):
        assert is_valid_email("123@example.com") is True

    def test_hyphen_in_domain(self):
        assert is_valid_email("user@my-domain.org") is True

    def test_two_letter_tld(self):
        assert is_valid_email("user@example.io") is True

    # --- invalid addresses ---
    def test_empty_string(self):
        assert is_valid_email("") is False

    def test_no_at_sign(self):
        assert is_valid_email("userexample.com") is False

    def test_no_domain(self):
        assert is_valid_email("user@") is False

    def test_no_local_part(self):
        assert is_valid_email("@example.com") is False

    def test_no_tld(self):
        assert is_valid_email("user@example") is False

    def test_spaces(self):
        assert is_valid_email("user @example.com") is False

    def test_too_long(self):
        local = "a" * 250
        assert is_valid_email(f"{local}@example.com") is False

    def test_non_string(self):
        assert is_valid_email(None) is False  # type: ignore[arg-type]

    def test_non_string_int(self):
        assert is_valid_email(42) is False  # type: ignore[arg-type]

    def test_consecutive_dots_in_local(self):
        assert is_valid_email("user..name@example.com") is False

    def test_consecutive_dots_in_domain(self):
        assert is_valid_email("user@example..com") is False

    def test_dot_at_start_of_local(self):
        assert is_valid_email(".user@example.com") is False

    def test_dot_at_end_of_local(self):
        assert is_valid_email("user.@example.com") is False

    def test_hyphen_at_start_of_domain_label(self):
        assert is_valid_email("user@-example.com") is False

    def test_hyphen_at_end_of_domain_label(self):
        assert is_valid_email("user@example-.com") is False


class TestValidateEmail:
    """Tests for validate_email()."""

    def test_valid_returns_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_strips_whitespace(self):
        assert validate_email("  user@example.com  ") == "user@example.com"

    def test_invalid_raises(self):
        with pytest.raises(InvalidEmailError):
            validate_email("not-an-email")

    def test_empty_raises(self):
        with pytest.raises(InvalidEmailError):
            validate_email("")

    def test_error_is_value_error(self):
        with pytest.raises(ValueError):
            validate_email("bad@")
