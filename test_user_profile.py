#!/usr/bin/env python3
"""Tests for the user_profile module."""

import unittest
from user_profile import create_profile, get_profile, update_profile


class TestCreateProfile(unittest.TestCase):

    def setUp(self):
        self.profiles = {}

    def test_create_profile_success(self):
        result = create_profile("user1", self.profiles)
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])
        self.assertIsInstance(result["profile"], dict)

    def test_create_profile_initialises_allowed_fields(self):
        create_profile("user1", self.profiles)
        result = get_profile("user1", self.profiles)
        for field in ("display_name", "bio", "location", "website"):
            self.assertIn(field, result["profile"])

    def test_create_profile_duplicate_returns_error(self):
        create_profile("user1", self.profiles)
        result = create_profile("user1", self.profiles)
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_create_profile_empty_user_id_returns_error(self):
        result = create_profile("", self.profiles)
        self.assertFalse(result["success"])
        self.assertIn("user id", result["error"].lower())

    def test_create_profile_whitespace_user_id_returns_error(self):
        result = create_profile("   ", self.profiles)
        self.assertFalse(result["success"])

    def test_create_profile_non_string_user_id_returns_error(self):
        result = create_profile(None, self.profiles)
        self.assertFalse(result["success"])

    def test_create_profile_invalid_store_returns_error(self):
        result = create_profile("user1", None)
        self.assertFalse(result["success"])

    def test_create_profile_strips_user_id(self):
        create_profile("  user1  ", self.profiles)
        self.assertIn("user1", self.profiles)


class TestGetProfile(unittest.TestCase):

    def setUp(self):
        self.profiles = {}
        create_profile("user1", self.profiles)

    def test_get_profile_success(self):
        result = get_profile("user1", self.profiles)
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])
        self.assertIsInstance(result["profile"], dict)

    def test_get_profile_not_found_returns_error(self):
        result = get_profile("unknown", self.profiles)
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])
        self.assertIsNone(result["profile"])

    def test_get_profile_empty_user_id_returns_error(self):
        result = get_profile("", self.profiles)
        self.assertFalse(result["success"])

    def test_get_profile_none_user_id_returns_error(self):
        result = get_profile(None, self.profiles)
        self.assertFalse(result["success"])

    def test_get_profile_invalid_store_returns_error(self):
        result = get_profile("user1", None)
        self.assertFalse(result["success"])

    def test_get_profile_returns_copy(self):
        result = get_profile("user1", self.profiles)
        result["profile"]["display_name"] = "tampered"
        self.assertEqual(self.profiles["user1"]["display_name"], "")


class TestUpdateProfile(unittest.TestCase):

    def setUp(self):
        self.profiles = {}
        create_profile("user1", self.profiles)

    def test_update_display_name(self):
        result = update_profile("user1", {"display_name": "Alice"}, self.profiles)
        self.assertTrue(result["success"])
        self.assertEqual(result["profile"]["display_name"], "Alice")

    def test_update_multiple_fields(self):
        result = update_profile(
            "user1",
            {"display_name": "Alice", "bio": "Hello!", "location": "Wonderland"},
            self.profiles,
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["profile"]["display_name"], "Alice")
        self.assertEqual(result["profile"]["bio"], "Hello!")
        self.assertEqual(result["profile"]["location"], "Wonderland")

    def test_update_strips_whitespace(self):
        result = update_profile("user1", {"display_name": "  Alice  "}, self.profiles)
        self.assertTrue(result["success"])
        self.assertEqual(result["profile"]["display_name"], "Alice")

    def test_update_unknown_field_returns_error(self):
        result = update_profile("user1", {"age": "30"}, self.profiles)
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_update_non_string_value_returns_error(self):
        result = update_profile("user1", {"display_name": 123}, self.profiles)
        self.assertFalse(result["success"])
        self.assertIn("string", result["error"].lower())

    def test_update_value_exceeds_max_length_returns_error(self):
        long_name = "a" * 101
        result = update_profile("user1", {"display_name": long_name}, self.profiles)
        self.assertFalse(result["success"])
        self.assertIn("length", result["error"].lower())

    def test_update_profile_not_found_returns_error(self):
        result = update_profile("ghost", {"display_name": "Ghost"}, self.profiles)
        self.assertFalse(result["success"])
        self.assertIsNone(result["profile"])

    def test_update_empty_user_id_returns_error(self):
        result = update_profile("", {"display_name": "Alice"}, self.profiles)
        self.assertFalse(result["success"])

    def test_update_non_dict_updates_returns_error(self):
        result = update_profile("user1", "display_name=Alice", self.profiles)
        self.assertFalse(result["success"])

    def test_update_invalid_store_returns_error(self):
        result = update_profile("user1", {"display_name": "Alice"}, None)
        self.assertFalse(result["success"])

    def test_update_does_not_affect_other_users(self):
        create_profile("user2", self.profiles)
        update_profile("user1", {"display_name": "Alice"}, self.profiles)
        result = get_profile("user2", self.profiles)
        self.assertEqual(result["profile"]["display_name"], "")

    def test_update_returns_copy_not_reference(self):
        result = update_profile("user1", {"display_name": "Alice"}, self.profiles)
        result["profile"]["display_name"] = "tampered"
        self.assertEqual(self.profiles["user1"]["display_name"], "Alice")


if __name__ == "__main__":
    unittest.main()
