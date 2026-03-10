#!/usr/bin/env python3
"""Tests for the email_validator module."""

import unittest
from email_validator import is_valid_email


class TestIsValidEmail(unittest.TestCase):
    # --- valid addresses ---
    def test_simple_valid(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_subdomain(self):
        self.assertTrue(is_valid_email("user@mail.example.com"))

    def test_plus_tag(self):
        self.assertTrue(is_valid_email("user+tag@example.com"))

    def test_dots_in_local(self):
        self.assertTrue(is_valid_email("first.last@example.com"))

    def test_long_tld(self):
        self.assertTrue(is_valid_email("user@example.museum"))

    def test_hyphen_in_domain(self):
        self.assertTrue(is_valid_email("user@my-domain.org"))

    def test_numeric_local(self):
        self.assertTrue(is_valid_email("123@example.com"))

    def test_special_chars_in_local(self):
        self.assertTrue(is_valid_email("user.name+filter@example.co.uk"))

    # --- invalid addresses ---
    def test_missing_at(self):
        self.assertFalse(is_valid_email("userexample.com"))

    def test_missing_domain(self):
        self.assertFalse(is_valid_email("user@"))

    def test_missing_local(self):
        self.assertFalse(is_valid_email("@example.com"))

    def test_missing_tld(self):
        self.assertFalse(is_valid_email("user@example"))

    def test_consecutive_dots_in_local(self):
        self.assertFalse(is_valid_email("us..er@example.com"))

    def test_consecutive_dots_in_domain(self):
        self.assertFalse(is_valid_email("user@ex..ample.com"))

    def test_leading_dot_in_local(self):
        self.assertFalse(is_valid_email(".user@example.com"))

    def test_trailing_dot_in_local(self):
        self.assertFalse(is_valid_email("user.@example.com"))

    def test_single_char_tld(self):
        self.assertFalse(is_valid_email("user@example.c"))

    def test_numeric_tld(self):
        self.assertFalse(is_valid_email("user@example.123"))

    def test_empty_string(self):
        self.assertFalse(is_valid_email(""))

    def test_non_string_input(self):
        self.assertFalse(is_valid_email(None))
        self.assertFalse(is_valid_email(123))

    def test_exceeds_max_length(self):
        # 244 + len("@example.com") = 256 > 254 character RFC 5321 limit
        local = "a" * 244
        self.assertFalse(is_valid_email(f"{local}@example.com"))

    def test_whitespace(self):
        self.assertFalse(is_valid_email("user @example.com"))
        self.assertFalse(is_valid_email("user@ example.com"))


if __name__ == "__main__":
    unittest.main()
