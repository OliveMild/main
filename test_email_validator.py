#!/usr/bin/env python3
import unittest
from email_validator import is_valid_email


class TestIsValidEmail(unittest.TestCase):

    def test_valid_emails(self):
        valid = [
            "user@example.com",
            "user.name+tag@sub.domain.org",
            "user_123@domain.co",
            "USER@DOMAIN.COM",
        ]
        for email in valid:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email))

    def test_invalid_emails(self):
        invalid = [
            "",
            "notanemail",
            "@nodomain.com",
            "user@",
            "user@domain",
            "user @domain.com",
            ".user@domain.com",
            "user.@domain.com",
            "user@domain..com",
            "user@.domain.com",
            None,
            123,
        ]
        for email in invalid:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email))


if __name__ == "__main__":
    unittest.main()
