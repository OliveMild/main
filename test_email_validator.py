#!/usr/bin/env python3
"""Tests for the email_validator module."""

import pytest

from email_validator import EmailValidationError, validate_email


# ---------------------------------------------------------------------------
# Valid emails
# ---------------------------------------------------------------------------

class TestValidEmails:
    def test_simple_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_email_normalized_to_lowercase(self):
        assert validate_email("User@Example.COM") == "user@example.com"

    def test_email_with_plus_tag(self):
        assert validate_email("alice+tag@example.com") == "alice+tag@example.com"

    def test_email_with_dots_in_local(self):
        assert validate_email("first.last@example.com") == "first.last@example.com"

    def test_email_with_subdomain(self):
        assert validate_email("user@mail.example.com") == "user@mail.example.com"

    def test_email_with_hyphen_in_domain(self):
        assert validate_email("user@my-domain.com") == "user@my-domain.com"

    def test_email_strips_surrounding_whitespace(self):
        assert validate_email("  user@example.com  ") == "user@example.com"

    def test_email_with_numbers(self):
        assert validate_email("user123@example456.org") == "user123@example456.org"


# ---------------------------------------------------------------------------
# Invalid emails
# ---------------------------------------------------------------------------

class TestInvalidEmails:
    def test_missing_at_sign(self):
        with pytest.raises(EmailValidationError):
            validate_email("userexample.com")

    def test_double_at_sign(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@@example.com")

    def test_empty_local_part(self):
        with pytest.raises(EmailValidationError):
            validate_email("@example.com")

    def test_empty_domain_part(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@")

    def test_no_dot_in_domain(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@localhost")

    def test_consecutive_dots_in_domain(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@exam..ple.com")

    def test_domain_starts_with_dot(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@.example.com")

    def test_domain_ends_with_dot(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@example.com.")

    def test_domain_starts_with_hyphen(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@-example.com")

    def test_domain_ends_with_hyphen(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@example-.com")

    def test_whitespace_in_local_part(self):
        with pytest.raises(EmailValidationError):
            validate_email("user name@example.com")

    def test_whitespace_in_domain(self):
        with pytest.raises(EmailValidationError):
            validate_email("user@exam ple.com")

    def test_non_string_input(self):
        with pytest.raises(EmailValidationError):
            validate_email(12345)

    def test_none_input(self):
        with pytest.raises(EmailValidationError):
            validate_email(None)

    def test_empty_string(self):
        with pytest.raises(EmailValidationError):
            validate_email("")

    def test_email_exceeds_max_length(self):
        local = "a" * 200
        domain = "b" * 50 + ".com"
        with pytest.raises(EmailValidationError):
            validate_email(f"{local}@{domain}")
