#!/usr/bin/env python3
"""Tests for the email_validator module."""

import unittest
from email_validator import validate_email


class TestValidateEmail(unittest.TestCase):
    def test_valid_simple(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_valid_with_plus(self):
        self.assertTrue(validate_email("user+tag@example.com"))

    def test_valid_with_dots_in_local(self):
        self.assertTrue(validate_email("first.last@example.com"))

    def test_valid_subdomain(self):
        self.assertTrue(validate_email("user@mail.example.com"))

    def test_valid_numeric_local(self):
        self.assertTrue(validate_email("123@example.com"))

    def test_invalid_missing_at(self):
        self.assertFalse(validate_email("userexample.com"))

    def test_invalid_missing_domain(self):
        self.assertFalse(validate_email("user@"))

    def test_invalid_missing_local(self):
        self.assertFalse(validate_email("@example.com"))

    def test_invalid_empty_string(self):
        self.assertFalse(validate_email(""))

    def test_invalid_non_string(self):
        self.assertFalse(validate_email(None))
        self.assertFalse(validate_email(42))

    def test_invalid_no_tld(self):
        self.assertFalse(validate_email("user@example"))

    def test_invalid_spaces(self):
        self.assertFalse(validate_email("user @example.com"))


if __name__ == "__main__":
    unittest.main()
