#!/usr/bin/env python3
"""Tests for the email_validator module."""

import unittest

from email_validator import InvalidEmailError, is_valid_email, validate_email


class TestValidateEmail(unittest.TestCase):
    """Tests for validate_email()."""

    # ------------------------------------------------------------------
    # Valid addresses
    # ------------------------------------------------------------------

    def test_simple_valid_email(self):
        self.assertEqual(validate_email("user@example.com"), "user@example.com")

    def test_subdomain_email(self):
        self.assertEqual(
            validate_email("user@mail.example.com"), "user@mail.example.com"
        )

    def test_plus_addressing(self):
        self.assertEqual(
            validate_email("user+tag@example.com"), "user+tag@example.com"
        )

    def test_dot_in_local_part(self):
        self.assertEqual(
            validate_email("first.last@example.com"), "first.last@example.com"
        )

    def test_whitespace_stripped(self):
        self.assertEqual(validate_email("  user@example.com  "), "user@example.com")

    def test_uppercase_letters(self):
        self.assertEqual(validate_email("User@Example.COM"), "User@Example.COM")

    def test_numeric_local_part(self):
        self.assertEqual(validate_email("123@example.com"), "123@example.com")

    # ------------------------------------------------------------------
    # Invalid addresses
    # ------------------------------------------------------------------

    def test_empty_string_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("   ")

    def test_missing_at_sign_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("userexample.com")

    def test_missing_domain_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("user@")

    def test_missing_local_part_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("@example.com")

    def test_missing_tld_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("user@example")

    def test_double_at_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("user@@example.com")

    def test_non_string_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email(None)  # type: ignore[arg-type]

    def test_space_in_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email("us er@example.com")


class TestIsValidEmail(unittest.TestCase):
    """Tests for is_valid_email()."""

    def test_valid_returns_true(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_invalid_returns_false(self):
        self.assertFalse(is_valid_email("not-an-email"))

    def test_empty_returns_false(self):
        self.assertFalse(is_valid_email(""))

    def test_none_returns_false(self):
        self.assertFalse(is_valid_email(None))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
