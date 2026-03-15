#!/usr/bin/env python3
"""Tests for the user_profile module."""

import unittest

from user_profile import ProfileError, create_profile, get_display_name, update_profile


class TestCreateProfile(unittest.TestCase):
    def test_create_valid_profile(self):
        profile = create_profile("alice", "alice@example.com")
        self.assertEqual(profile["username"], "alice")
        self.assertEqual(profile["email"], "alice@example.com")

    def test_create_profile_with_optional_fields(self):
        profile = create_profile(
            "bob",
            "bob@example.com",
            bio="Software engineer",
            location="New York",
            website="https://bob.dev",
        )
        self.assertEqual(profile["bio"], "Software engineer")
        self.assertEqual(profile["location"], "New York")
        self.assertEqual(profile["website"], "https://bob.dev")

    def test_create_profile_strips_whitespace(self):
        profile = create_profile("  carol  ", "  carol@example.com  ")
        self.assertEqual(profile["username"], "carol")
        self.assertEqual(profile["email"], "carol@example.com")

    def test_create_profile_empty_username_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("", "user@example.com")

    def test_create_profile_whitespace_username_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("   ", "user@example.com")

    def test_create_profile_none_username_raises(self):
        with self.assertRaises(ProfileError):
            create_profile(None, "user@example.com")

    def test_create_profile_long_username_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("a" * 51, "user@example.com")

    def test_create_profile_invalid_email_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("dave", "not-an-email")

    def test_create_profile_empty_email_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("eve", "")

    def test_create_profile_none_email_raises(self):
        with self.assertRaises(ProfileError):
            create_profile("frank", None)

    def test_create_profile_defaults_empty_optional_fields(self):
        profile = create_profile("grace", "grace@example.com")
        self.assertEqual(profile["bio"], "")
        self.assertEqual(profile["location"], "")
        self.assertEqual(profile["website"], "")


class TestUpdateProfile(unittest.TestCase):
    def setUp(self):
        self.profile = create_profile("alice", "alice@example.com", bio="Hello")

    def test_update_username(self):
        updated = update_profile(self.profile, username="alicia")
        self.assertEqual(updated["username"], "alicia")

    def test_update_email(self):
        updated = update_profile(self.profile, email="alicia@example.com")
        self.assertEqual(updated["email"], "alicia@example.com")

    def test_update_bio(self):
        updated = update_profile(self.profile, bio="New bio")
        self.assertEqual(updated["bio"], "New bio")

    def test_update_does_not_mutate_original(self):
        update_profile(self.profile, bio="Changed")
        self.assertEqual(self.profile["bio"], "Hello")

    def test_update_invalid_username_raises(self):
        with self.assertRaises(ProfileError):
            update_profile(self.profile, username="")

    def test_update_invalid_email_raises(self):
        with self.assertRaises(ProfileError):
            update_profile(self.profile, email="bad-email")

    def test_update_unknown_field_raises(self):
        with self.assertRaises(ValueError):
            update_profile(self.profile, nickname="ali")

    def test_update_non_dict_profile_raises(self):
        with self.assertRaises(ProfileError):
            update_profile("not-a-dict", username="alice")

    def test_update_multiple_fields(self):
        updated = update_profile(self.profile, bio="Updated", location="Berlin")
        self.assertEqual(updated["bio"], "Updated")
        self.assertEqual(updated["location"], "Berlin")


class TestGetDisplayName(unittest.TestCase):
    def test_returns_username(self):
        profile = create_profile("alice", "alice@example.com")
        self.assertEqual(get_display_name(profile), "alice")

    def test_returns_unknown_for_non_dict(self):
        self.assertEqual(get_display_name(None), "Unknown User")
        self.assertEqual(get_display_name("string"), "Unknown User")

    def test_returns_unknown_for_empty_username(self):
        self.assertEqual(get_display_name({"username": ""}), "Unknown User")
        self.assertEqual(get_display_name({"username": "   "}), "Unknown User")

    def test_returns_unknown_when_username_missing(self):
        self.assertEqual(get_display_name({}), "Unknown User")


if __name__ == "__main__":
    unittest.main()
