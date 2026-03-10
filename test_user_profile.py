#!/usr/bin/env python3
"""Tests for the user_profile module."""

import os
import tempfile
import unittest

from user_profile import create_profile, delete_profile, load_profile, update_profile


class TestCreateProfile(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(self.filepath)  # Remove so we start fresh

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_create_valid_profile(self):
        profile = create_profile("Alice", "alice@example.com", self.filepath)
        self.assertEqual(profile["name"], "Alice")
        self.assertEqual(profile["email"], "alice@example.com")

    def test_create_persists_to_file(self):
        create_profile("Bob", "bob@example.com", self.filepath)
        loaded = load_profile(self.filepath)
        self.assertEqual(loaded["name"], "Bob")
        self.assertEqual(loaded["email"], "bob@example.com")

    def test_create_strips_whitespace(self):
        profile = create_profile("  Alice  ", "  alice@example.com  ", self.filepath)
        self.assertEqual(profile["name"], "Alice")
        self.assertEqual(profile["email"], "alice@example.com")

    def test_create_name_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            create_profile(123, "a@b.com", self.filepath)

    def test_create_email_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            create_profile("Alice", 99, self.filepath)

    def test_create_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("", "a@b.com", self.filepath)

    def test_create_whitespace_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("   ", "a@b.com", self.filepath)

    def test_create_invalid_email_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "not-an-email", self.filepath)

    def test_create_email_missing_local_part_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "@example.com", self.filepath)

    def test_create_email_missing_domain_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "alice@", self.filepath)

    def test_create_email_double_at_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "alice@@example.com", self.filepath)

    def test_create_empty_email_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "", self.filepath)


class TestLoadProfile(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_load_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_profile(self.filepath)

    def test_load_corrupt_file_raises_value_error(self):
        with open(self.filepath, "w") as f:
            f.write("not valid json{{{")
        with self.assertRaises(ValueError):
            load_profile(self.filepath)

    def test_load_missing_fields_raises_value_error(self):
        import json
        with open(self.filepath, "w") as f:
            json.dump({"name": "Alice"}, f)
        with self.assertRaises(ValueError) as ctx:
            load_profile(self.filepath)
        self.assertIn("email", str(ctx.exception))

    def test_load_valid_profile(self):
        create_profile("Carol", "carol@example.com", self.filepath)
        profile = load_profile(self.filepath)
        self.assertEqual(profile["name"], "Carol")
        self.assertEqual(profile["email"], "carol@example.com")


class TestUpdateProfile(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(self.filepath)
        create_profile("Dave", "dave@example.com", self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_update_name(self):
        profile = update_profile({"name": "David"}, self.filepath)
        self.assertEqual(profile["name"], "David")
        self.assertEqual(profile["email"], "dave@example.com")

    def test_update_email(self):
        profile = update_profile({"email": "david@example.com"}, self.filepath)
        self.assertEqual(profile["email"], "david@example.com")

    def test_update_persists(self):
        update_profile({"name": "David"}, self.filepath)
        loaded = load_profile(self.filepath)
        self.assertEqual(loaded["name"], "David")

    def test_update_not_dict_raises_type_error(self):
        with self.assertRaises(TypeError):
            update_profile("name=David", self.filepath)

    def test_update_name_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            update_profile({"name": 42}, self.filepath)

    def test_update_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_profile({"name": ""}, self.filepath)

    def test_update_invalid_email_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_profile({"email": "bad-email"}, self.filepath)

    def test_update_email_missing_local_part_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_profile({"email": "@example.com"}, self.filepath)

    def test_update_email_missing_domain_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_profile({"email": "dave@"}, self.filepath)

    def test_update_nonexistent_profile_raises_file_not_found(self):
        os.unlink(self.filepath)
        with self.assertRaises(FileNotFoundError):
            update_profile({"name": "X"}, self.filepath)


class TestDeleteProfile(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(self.filepath)
        create_profile("Eve", "eve@example.com", self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_delete_removes_file(self):
        delete_profile(self.filepath)
        self.assertFalse(os.path.exists(self.filepath))

    def test_delete_missing_profile_raises_file_not_found(self):
        os.unlink(self.filepath)
        with self.assertRaises(FileNotFoundError):
            delete_profile(self.filepath)

    def test_delete_then_load_raises_file_not_found(self):
        delete_profile(self.filepath)
        with self.assertRaises(FileNotFoundError):
            load_profile(self.filepath)


if __name__ == "__main__":
    unittest.main()
