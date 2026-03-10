#!/usr/bin/env python3
"""Unit tests for email_validator.py."""

import unittest
from email_validator import validate_email


class TestValidateEmail(unittest.TestCase):

    # --- valid addresses ---

    def test_simple_valid(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_subdomain(self):
        self.assertTrue(validate_email("user@mail.example.com"))

    def test_plus_tag(self):
        self.assertTrue(validate_email("user+tag@example.com"))

    def test_dot_in_local(self):
        self.assertTrue(validate_email("first.last@example.com"))

    def test_numeric_local(self):
        self.assertTrue(validate_email("123@example.com"))

    def test_hyphen_in_domain(self):
        self.assertTrue(validate_email("user@my-domain.org"))

    def test_long_tld(self):
        self.assertTrue(validate_email("user@example.museum"))

    # --- invalid addresses ---

    def test_none_input(self):
        self.assertFalse(validate_email(None))

    def test_integer_input(self):
        self.assertFalse(validate_email(42))

    def test_empty_string(self):
        self.assertFalse(validate_email(""))

    def test_no_at_sign(self):
        self.assertFalse(validate_email("userexample.com"))

    def test_multiple_at_signs(self):
        self.assertFalse(validate_email("user@@example.com"))

    def test_space_in_email(self):
        self.assertFalse(validate_email("user @example.com"))

    def test_missing_domain(self):
        self.assertFalse(validate_email("user@"))

    def test_missing_local(self):
        self.assertFalse(validate_email("@example.com"))

    def test_consecutive_dots_local(self):
        self.assertFalse(validate_email("user..name@example.com"))

    def test_consecutive_dots_domain(self):
        self.assertFalse(validate_email("user@exam..ple.com"))

    def test_no_tld(self):
        self.assertFalse(validate_email("user@example"))

    def test_exceeds_max_length(self):
        long_local = "a" * 310
        self.assertFalse(validate_email(f"{long_local}@example.com"))

    def test_single_char_tld(self):
        self.assertFalse(validate_email("user@example.c"))

    def test_leading_dot_in_local(self):
        self.assertFalse(validate_email(".user@example.com"))

    def test_trailing_dot_in_local(self):
        self.assertFalse(validate_email("user.@example.com"))

    def test_leading_dot_in_domain(self):
        self.assertFalse(validate_email("user@.example.com"))

    def test_trailing_dot_in_domain(self):
        self.assertFalse(validate_email("user@example.com."))


if __name__ == "__main__":
    unittest.main()
