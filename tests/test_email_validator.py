"""Tests for email_validator module."""

import pytest
from email_validator import validate_email


class TestValidEmails:
    """Valid email addresses should return True."""

    def test_simple_email(self):
        assert validate_email("user@example.com") is True

    def test_email_with_subdomain(self):
        assert validate_email("user@mail.example.com") is True

    def test_email_with_plus(self):
        assert validate_email("user+tag@example.com") is True

    def test_email_with_dots_in_local(self):
        assert validate_email("first.last@example.com") is True

    def test_email_with_numbers(self):
        assert validate_email("user123@example456.com") is True

    def test_email_with_hyphen_in_domain(self):
        assert validate_email("user@my-domain.org") is True

    def test_email_with_long_tld(self):
        assert validate_email("user@example.travel") is True

    def test_email_with_underscore(self):
        assert validate_email("user_name@example.com") is True


class TestInvalidEmails:
    """Invalid email addresses should return False."""

    def test_missing_at_sign(self):
        assert validate_email("userexample.com") is False

    def test_missing_domain(self):
        assert validate_email("user@") is False

    def test_missing_local_part(self):
        assert validate_email("@example.com") is False

    def test_missing_tld(self):
        assert validate_email("user@example") is False

    def test_empty_string(self):
        assert validate_email("") is False

    def test_none_value(self):
        assert validate_email(None) is False

    def test_non_string_value(self):
        assert validate_email(12345) is False

    def test_double_at_sign(self):
        assert validate_email("user@@example.com") is False

    def test_spaces_in_email(self):
        assert validate_email("user @example.com") is False

    def test_single_char_tld(self):
        # TLDs must be at least 2 characters; single-char TLDs are not currently in use
        assert validate_email("user@example.c") is False
