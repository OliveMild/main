#!/usr/bin/env python3
"""Tests for the registration module."""

import unittest
from registration import validate_email, register_user


class TestValidateEmail(unittest.TestCase):

    # --- valid cases ---
    def test_simple_valid_email(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_email_with_subdomain(self):
        self.assertTrue(validate_email("user@mail.example.com"))

    def test_email_with_plus(self):
        self.assertTrue(validate_email("user+tag@example.com"))

    def test_email_with_dots_in_local(self):
        self.assertTrue(validate_email("first.last@example.org"))

    def test_email_with_numbers(self):
        self.assertTrue(validate_email("user123@example.co.uk"))

    def test_email_with_hyphen_in_domain(self):
        self.assertTrue(validate_email("user@my-domain.com"))

    def test_email_with_leading_trailing_spaces_stripped(self):
        self.assertTrue(validate_email("  user@example.com  "))

    # --- invalid cases ---
    def test_missing_at_symbol(self):
        self.assertFalse(validate_email("userexample.com"))

    def test_missing_domain(self):
        self.assertFalse(validate_email("user@"))

    def test_missing_local_part(self):
        self.assertFalse(validate_email("@example.com"))

    def test_missing_tld(self):
        self.assertFalse(validate_email("user@example"))

    def test_multiple_at_symbols(self):
        self.assertFalse(validate_email("user@@example.com"))

    def test_spaces_inside_email(self):
        self.assertFalse(validate_email("us er@example.com"))

    def test_empty_string(self):
        self.assertFalse(validate_email(""))

    def test_non_string_input(self):
        self.assertFalse(validate_email(None))
        self.assertFalse(validate_email(123))

    def test_tld_too_short(self):
        self.assertFalse(validate_email("user@example.c"))


class TestRegisterUser(unittest.TestCase):

    def test_successful_registration(self):
        result = register_user("alice", "alice@example.com")
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])

    def test_invalid_email_returns_error(self):
        result = register_user("bob", "not-an-email")
        self.assertFalse(result["success"])
        self.assertIn("email", result["error"].lower())

    def test_empty_username_returns_error(self):
        result = register_user("", "user@example.com")
        self.assertFalse(result["success"])
        self.assertIn("username", result["error"].lower())

    def test_whitespace_username_returns_error(self):
        result = register_user("   ", "user@example.com")
        self.assertFalse(result["success"])
        self.assertIn("username", result["error"].lower())


if __name__ == "__main__":
    unittest.main()
