#!/usr/bin/env python3
"""Tests for the email_validator and user_registration modules."""

import unittest
from email_validator import is_valid_email
from user_registration import register_user


class TestIsValidEmail(unittest.TestCase):

    # --- valid cases ---
    def test_simple_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_email_with_subdomain(self):
        self.assertTrue(is_valid_email("user@mail.example.com"))

    def test_email_with_plus(self):
        self.assertTrue(is_valid_email("user+tag@example.com"))

    def test_email_with_dots_in_local(self):
        self.assertTrue(is_valid_email("first.last@example.org"))

    def test_email_with_numbers(self):
        self.assertTrue(is_valid_email("user123@example.co.uk"))

    def test_email_with_hyphen_in_domain(self):
        self.assertTrue(is_valid_email("user@my-domain.com"))

    def test_email_uppercase(self):
        self.assertTrue(is_valid_email("USER@EXAMPLE.COM"))

    def test_email_with_leading_trailing_spaces_stripped(self):
        self.assertTrue(is_valid_email("  user@example.com  "))

    # --- invalid cases ---
    def test_missing_at_symbol(self):
        self.assertFalse(is_valid_email("userexample.com"))

    def test_missing_domain(self):
        self.assertFalse(is_valid_email("user@"))

    def test_missing_local_part(self):
        self.assertFalse(is_valid_email("@example.com"))

    def test_missing_tld(self):
        self.assertFalse(is_valid_email("user@example"))

    def test_tld_too_short(self):
        self.assertFalse(is_valid_email("user@example.c"))

    def test_multiple_at_symbols(self):
        self.assertFalse(is_valid_email("user@@example.com"))

    def test_consecutive_dots_in_local(self):
        self.assertFalse(is_valid_email("user..name@example.com"))

    def test_consecutive_dots_in_domain(self):
        self.assertFalse(is_valid_email("user@example..com"))

    def test_spaces_inside_email(self):
        self.assertFalse(is_valid_email("us er@example.com"))

    def test_empty_string(self):
        self.assertFalse(is_valid_email(""))

    def test_whitespace_only(self):
        self.assertFalse(is_valid_email("   "))

    def test_none_input(self):
        self.assertFalse(is_valid_email(None))

    def test_integer_input(self):
        self.assertFalse(is_valid_email(123))

    def test_domain_starting_with_dot(self):
        self.assertFalse(is_valid_email("user@.example.com"))

    def test_domain_label_leading_hyphen(self):
        self.assertFalse(is_valid_email("user@-example.com"))

    def test_domain_label_trailing_hyphen(self):
        self.assertFalse(is_valid_email("user@example-.com"))


class TestRegisterUser(unittest.TestCase):

    def test_successful_registration(self):
        result = register_user("alice", "alice@example.com")
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])
        self.assertEqual(result["username"], "alice")
        self.assertEqual(result["email"], "alice@example.com")

    def test_invalid_email_does_not_leak_email(self):
        result = register_user("bob", "not-an-email")
        self.assertFalse(result["success"])
        self.assertIn("email", result["error"].lower())
        self.assertNotIn("not-an-email", result["error"])

    def test_empty_username_returns_error(self):
        result = register_user("", "user@example.com")
        self.assertFalse(result["success"])
        self.assertIn("username", result["error"].lower())

    def test_whitespace_username_returns_error(self):
        result = register_user("   ", "user@example.com")
        self.assertFalse(result["success"])
        self.assertIn("username", result["error"].lower())

    def test_non_string_username_returns_error(self):
        result = register_user(None, "user@example.com")
        self.assertFalse(result["success"])
        self.assertIn("username", result["error"].lower())

    def test_username_whitespace_stripped(self):
        result = register_user("  alice  ", "alice@example.com")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], "alice")

    def test_invalid_username_does_not_leak_email(self):
        result = register_user("", "secret@example.com")
        self.assertFalse(result["success"])
        self.assertNotIn("secret@example.com", result["error"])

    def test_email_whitespace_stripped(self):
        result = register_user("alice", "  alice@example.com  ")
        self.assertTrue(result["success"])
        self.assertEqual(result["email"], "alice@example.com")

    def test_invalid_email_does_not_leak_username(self):
        result = register_user("secretuser", "not-an-email")
        self.assertFalse(result["success"])
        self.assertNotIn("secretuser", result["error"])


if __name__ == "__main__":
    unittest.main()
