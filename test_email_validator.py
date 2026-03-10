#!/usr/bin/env python3
"""Tests for email_validator module."""

import pytest

from email_validator import InvalidEmailError, is_valid_email, validate_email


class TestIsValidEmail:
    def test_valid_simple(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_subdomain(self):
        assert is_valid_email("user@mail.example.co.uk") is True

    def test_valid_plus_tag(self):
        assert is_valid_email("user+tag@mail.example.co.uk") is True

    def test_invalid_no_at(self):
        assert is_valid_email("not-an-email") is False

    def test_invalid_double_at(self):
        assert is_valid_email("bad@@addr") is False

    def test_invalid_none(self):
        assert is_valid_email(None) is False

    def test_invalid_empty_string(self):
        assert is_valid_email("") is False

    def test_invalid_int(self):
        assert is_valid_email(42) is False

    def test_invalid_consecutive_dots_local(self):
        assert is_valid_email("user..name@example.com") is False

    def test_invalid_leading_dot_local(self):
        assert is_valid_email(".user@example.com") is False

    def test_invalid_trailing_dot_local(self):
        assert is_valid_email("user.@example.com") is False

    def test_invalid_consecutive_dots_domain(self):
        assert is_valid_email("user@ex..ample.com") is False

    def test_invalid_domain_label_starts_with_hyphen(self):
        assert is_valid_email("user@-example.com") is False

    def test_invalid_domain_label_ends_with_hyphen(self):
        assert is_valid_email("user@example-.com") is False


class TestValidateEmail:
    def test_valid_email_returned(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_invalid_raises(self):
        with pytest.raises(InvalidEmailError):
            validate_email("bad@@addr")

    def test_error_message(self):
        with pytest.raises(InvalidEmailError, match="Invalid email address: 'bad@@addr'"):
            validate_email("bad@@addr")

    def test_invalid_none_raises(self):
        with pytest.raises(InvalidEmailError):
            validate_email(None)
