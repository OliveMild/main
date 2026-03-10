#!/usr/bin/env python3
"""Tests for the user_profile module."""

import unittest
from user_profile import UserProfile, UserProfileError


class TestUserProfileCreation(unittest.TestCase):
    """Tests for creating UserProfile instances."""

    def test_valid_profile(self):
        profile = UserProfile("alice", "alice@example.com")
        self.assertEqual(profile.username, "alice")
        self.assertEqual(profile.email, "alice@example.com")
        self.assertEqual(profile.bio, "")

    def test_valid_profile_with_bio(self):
        profile = UserProfile("bob", "bob@example.com", bio="Software developer.")
        self.assertEqual(profile.bio, "Software developer.")

    def test_username_is_stripped(self):
        profile = UserProfile("  carol  ", "carol@example.com")
        self.assertEqual(profile.username, "carol")

    def test_empty_username_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("", "user@example.com")

    def test_whitespace_username_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("   ", "user@example.com")

    def test_none_username_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile(None, "user@example.com")

    def test_username_too_long_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("a" * 51, "user@example.com")

    def test_invalid_email_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("dave", "not-an-email")

    def test_none_email_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("eve", None)

    def test_email_missing_at_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("frank", "frankexample.com")

    def test_email_with_spaces_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("grace", "grace @example.com")

    def test_email_consecutive_dots_in_domain_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("hal", "hal@example..com")

    def test_bio_too_long_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("ivan", "ivan@example.com", bio="x" * 501)

    def test_non_string_bio_raises(self):
        with self.assertRaises(UserProfileError):
            UserProfile("judy", "judy@example.com", bio=42)


class TestGetProfile(unittest.TestCase):
    """Tests for UserProfile.get_profile()."""

    def test_returns_dict(self):
        profile = UserProfile("alice", "alice@example.com", bio="Hello")
        data = profile.get_profile()
        self.assertIsInstance(data, dict)

    def test_dict_contains_expected_keys(self):
        profile = UserProfile("alice", "alice@example.com")
        data = profile.get_profile()
        self.assertIn("username", data)
        self.assertIn("email", data)
        self.assertIn("bio", data)

    def test_dict_values_match_profile(self):
        profile = UserProfile("alice", "alice@example.com", bio="Dev")
        data = profile.get_profile()
        self.assertEqual(data["username"], "alice")
        self.assertEqual(data["email"], "alice@example.com")
        self.assertEqual(data["bio"], "Dev")


class TestUpdateProfile(unittest.TestCase):
    """Tests for UserProfile.update_profile()."""

    def setUp(self):
        self.profile = UserProfile("alice", "alice@example.com", bio="")

    def test_update_username(self):
        self.profile.update_profile(username="alice2")
        self.assertEqual(self.profile.username, "alice2")

    def test_update_email(self):
        self.profile.update_profile(email="newalice@example.com")
        self.assertEqual(self.profile.email, "newalice@example.com")

    def test_update_bio(self):
        self.profile.update_profile(bio="Updated bio.")
        self.assertEqual(self.profile.bio, "Updated bio.")

    def test_partial_update_does_not_change_other_fields(self):
        self.profile.update_profile(bio="Just bio changed.")
        self.assertEqual(self.profile.username, "alice")
        self.assertEqual(self.profile.email, "alice@example.com")

    def test_update_with_invalid_email_raises(self):
        with self.assertRaises(UserProfileError):
            self.profile.update_profile(email="bad-email")

    def test_update_with_empty_username_raises(self):
        with self.assertRaises(UserProfileError):
            self.profile.update_profile(username="")

    def test_update_with_bio_too_long_raises(self):
        with self.assertRaises(UserProfileError):
            self.profile.update_profile(bio="x" * 501)

    def test_failed_update_leaves_profile_unchanged(self):
        original_email = self.profile.email
        try:
            self.profile.update_profile(email="invalid")
        except UserProfileError:
            pass
        self.assertEqual(self.profile.email, original_email)

    def test_update_no_args_changes_nothing(self):
        self.profile.update_profile()
        data = self.profile.get_profile()
        self.assertEqual(data["username"], "alice")
        self.assertEqual(data["email"], "alice@example.com")
        self.assertEqual(data["bio"], "")


if __name__ == "__main__":
    unittest.main()
