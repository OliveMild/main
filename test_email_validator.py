#!/usr/bin/env python3
import unittest
from email_validator import is_valid_email
from user_registration import register_user


class TestIsValidEmail(unittest.TestCase):
    def test_valid_emails(self):
        valid = [
            "user@example.com",
            "user.name+tag@sub.domain.org",
            "user_name@domain.co.uk",
            "USER@EXAMPLE.COM",
            "123@numbers.com",
        ]
        for email in valid:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email), f"Expected valid: {email}")

    def test_invalid_emails(self):
        invalid = [
            "",
            "notanemail",
            "@nodomain.com",
            "missing@",
            "missing.domain@",
            "two@@at.com",
            "user@.com",
            "user@com",
            "user..name@example.com",
            "user@example..com",
            ".user@example.com",
            "user.@example.com",
            "user@example.com.",
            None,
            123,
        ]
        for email in invalid:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email), f"Expected invalid: {email}")


class TestRegisterUser(unittest.TestCase):
    def test_successful_registration(self):
        result = register_user("alice", "alice@example.com")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], "alice")
        self.assertEqual(result["email"], "alice@example.com")

    def test_registration_with_invalid_email(self):
        result = register_user("bob", "not-an-email")
        self.assertFalse(result["success"])
        self.assertIn("Invalid email", result["error"])

    def test_empty_username(self):
        result = register_user("", "bob@example.com")
        self.assertFalse(result["success"])
        self.assertIn("Username is required", result["error"])

    def test_whitespace_username(self):
        result = register_user("   ", "bob@example.com")
        self.assertFalse(result["success"])
        self.assertIn("Username is required", result["error"])


if __name__ == "__main__":
    unittest.main()
