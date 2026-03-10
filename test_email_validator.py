#!/usr/bin/env python3
"""Tests for email validation and user registration."""

import unittest
from email_validator import is_valid_email
from user_registration import register_user


class TestIsValidEmail(unittest.TestCase):
    """Tests for the is_valid_email function."""

    # --- valid addresses ---

    def test_simple_valid_email(self):
        self.assertTrue(is_valid_email('user@example.com'))

    def test_valid_email_with_subdomain(self):
        self.assertTrue(is_valid_email('user@mail.example.com'))

    def test_valid_email_with_plus(self):
        self.assertTrue(is_valid_email('user+tag@example.com'))

    def test_valid_email_with_dots_in_local(self):
        self.assertTrue(is_valid_email('first.last@example.com'))

    def test_valid_email_with_hyphens(self):
        self.assertTrue(is_valid_email('user-name@my-domain.org'))

    # --- invalid addresses ---

    def test_invalid_email_missing_at(self):
        self.assertFalse(is_valid_email('userexample.com'))

    def test_invalid_email_missing_domain(self):
        self.assertFalse(is_valid_email('user@'))

    def test_invalid_email_missing_tld(self):
        self.assertFalse(is_valid_email('user@example'))

    def test_invalid_email_empty_string(self):
        self.assertFalse(is_valid_email(''))

    def test_invalid_email_none(self):
        self.assertFalse(is_valid_email(None))

    def test_invalid_email_with_space(self):
        self.assertFalse(is_valid_email('user @example.com'))

    def test_invalid_email_double_at(self):
        self.assertFalse(is_valid_email('user@@example.com'))

    def test_invalid_email_non_string(self):
        self.assertFalse(is_valid_email(42))


class TestRegisterUser(unittest.TestCase):
    """Tests for the register_user function."""

    def test_successful_registration(self):
        result = register_user('alice', 'alice@example.com', 'securepass')
        self.assertTrue(result['success'])
        self.assertIn('alice', result['message'])

    def test_invalid_email_returns_error(self):
        result = register_user('bob', 'not-an-email', 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Invalid email', result['message'])

    def test_empty_username_returns_error(self):
        result = register_user('', 'user@example.com', 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Username', result['message'])

    def test_whitespace_username_returns_error(self):
        result = register_user('   ', 'user@example.com', 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Username', result['message'])

    def test_short_password_returns_error(self):
        result = register_user('carol', 'carol@example.com', 'short')
        self.assertFalse(result['success'])
        self.assertIn('Password', result['message'])

    def test_none_email_returns_error(self):
        result = register_user('dave', None, 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Invalid email', result['message'])

    def test_none_username_returns_error(self):
        result = register_user(None, 'user@example.com', 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Username', result['message'])


if __name__ == '__main__':
    unittest.main()
