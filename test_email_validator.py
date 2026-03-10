#!/usr/bin/env python3
import unittest
from email_validator import is_valid_email


class TestIsValidEmail(unittest.TestCase):
    def test_valid_emails(self):
        valid = [
            "user@example.com",
            "user.name+tag@sub.domain.org",
            "USER@EXAMPLE.COM",
            "u@example.io",
            "user-name@example.co.uk",
        ]
        for email in valid:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email), f"Expected valid: {email}")

    def test_invalid_emails(self):
        invalid = [
            "",
            "notanemail",
            "@nodomain.com",
            "user@",
            "user@.com",
            "user@domain",
            "user @example.com",
            # consecutive/leading/trailing dots
            "user..name@example.com",
            ".user@example.com",
            "user.@example.com",
            # domain issues
            "user@domain..com",
            "user@-domain.com",
            "user@domain-.com",
            None,
            123,
        ]
        for email in invalid:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email), f"Expected invalid: {email}")

    def test_whitespace_stripped(self):
        self.assertTrue(is_valid_email("  user@example.com  "))


if __name__ == "__main__":
    unittest.main()
