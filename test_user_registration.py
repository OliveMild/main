#!/usr/bin/env python3
"""Unit tests for user_registration module."""

import unittest

from user_registration import validate_email, register_user


class TestValidateEmail(unittest.TestCase):
    # ------------------------------------------------------------------
    # Valid addresses
    # ------------------------------------------------------------------
    def test_simple_valid(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_subdomain(self):
        self.assertTrue(validate_email("user@mail.example.com"))

    def test_plus_addressing(self):
        self.assertTrue(validate_email("user+tag@example.com"))

    def test_dots_in_local(self):
        self.assertTrue(validate_email("first.last@example.com"))

    def test_hyphens_in_domain(self):
        self.assertTrue(validate_email("user@my-domain.org"))

    def test_numeric_local(self):
        self.assertTrue(validate_email("123@example.com"))

    def test_long_tld(self):
        self.assertTrue(validate_email("user@example.museum"))

    # ------------------------------------------------------------------
    # Invalid addresses
    # ------------------------------------------------------------------
    def test_none_input(self):
        self.assertFalse(validate_email(None))

    def test_integer_input(self):
        self.assertFalse(validate_email(42))

    def test_missing_at(self):
        self.assertFalse(validate_email("userexample.com"))

    def test_double_at(self):
        self.assertFalse(validate_email("user@@example.com"))

    def test_missing_tld(self):
        self.assertFalse(validate_email("user@example"))

    def test_space_in_email(self):
        self.assertFalse(validate_email("user @example.com"))

    def test_empty_string(self):
        self.assertFalse(validate_email(""))

    def test_consecutive_dots_in_local(self):
        self.assertFalse(validate_email("user..name@example.com"))

    def test_trailing_dot_in_local(self):
        self.assertFalse(validate_email("user.@example.com"))

    def test_leading_dot_in_local(self):
        self.assertFalse(validate_email(".user@example.com"))

    def test_single_char_tld(self):
        self.assertFalse(validate_email("user@example.c"))

    def test_missing_domain(self):
        self.assertFalse(validate_email("user@"))


class TestRegisterUser(unittest.TestCase):
    def test_successful_registration(self):
        result = register_user("alice", "alice@example.com", "securepass")
        self.assertTrue(result["success"])
        self.assertIn("alice", result["message"])

    def test_strips_whitespace_from_username(self):
        result = register_user("  bob  ", "bob@example.com", "securepass")
        self.assertTrue(result["success"])
        self.assertIn("bob", result["message"])

    def test_empty_username(self):
        result = register_user("", "user@example.com", "securepass")
        self.assertFalse(result["success"])
        self.assertIn("Username", result["message"])

    def test_whitespace_only_username(self):
        result = register_user("   ", "user@example.com", "securepass")
        self.assertFalse(result["success"])

    def test_none_username(self):
        result = register_user(None, "user@example.com", "securepass")
        self.assertFalse(result["success"])

    def test_invalid_email(self):
        result = register_user("charlie", "not-an-email", "securepass")
        self.assertFalse(result["success"])
        self.assertIn("email", result["message"].lower())

    def test_short_password(self):
        result = register_user("dave", "dave@example.com", "short")
        self.assertFalse(result["success"])
        self.assertIn("8", result["message"])
        self.assertIn("non-whitespace", result["message"])

    def test_none_password(self):
        result = register_user("eve", "eve@example.com", None)
        self.assertFalse(result["success"])

    def test_password_exactly_8_chars(self):
        result = register_user("frank", "frank@example.com", "12345678")
        self.assertTrue(result["success"])

    def test_password_with_spaces_too_short(self):
        # Spaces don't count toward password length
        result = register_user("grace", "grace@example.com", "1 2 3 4 ")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
