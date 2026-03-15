#!/usr/bin/env python3
"""Tests for user registration email validation."""

import unittest
from user_registration import validate_email, register_user


class TestValidateEmail(unittest.TestCase):
    """Tests for the validate_email function."""

    def test_valid_email(self):
        self.assertTrue(validate_email('user@example.com'))

    def test_valid_email_with_subdomain(self):
        self.assertTrue(validate_email('user@mail.example.com'))

    def test_valid_email_with_plus(self):
        self.assertTrue(validate_email('user+tag@example.com'))

    def test_valid_email_with_dots(self):
        self.assertTrue(validate_email('first.last@example.com'))

    def test_valid_email_with_hyphens(self):
        self.assertTrue(validate_email('user-name@my-domain.org'))

    def test_invalid_email_missing_at(self):
        self.assertFalse(validate_email('userexample.com'))

    def test_invalid_email_missing_domain(self):
        self.assertFalse(validate_email('user@'))

    def test_invalid_email_missing_tld(self):
        self.assertFalse(validate_email('user@example'))

    def test_invalid_email_empty_string(self):
        self.assertFalse(validate_email(''))

    def test_invalid_email_none(self):
        self.assertFalse(validate_email(None))

    def test_invalid_email_spaces(self):
        self.assertFalse(validate_email('user @example.com'))

    def test_invalid_email_double_at(self):
        self.assertFalse(validate_email('user@@example.com'))


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

    def test_short_password_returns_error(self):
        result = register_user('carol', 'carol@example.com', 'short')
        self.assertFalse(result['success'])
        self.assertIn('Password', result['message'])

    def test_none_email_returns_error(self):
        result = register_user('dave', None, 'securepass')
        self.assertFalse(result['success'])
        self.assertIn('Invalid email', result['message'])


if __name__ == '__main__':
    unittest.main()
