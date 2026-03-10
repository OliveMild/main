#!/usr/bin/env python3
"""Tests for the user_profile module."""

import json
import os
import tempfile
import unittest

from user_profile import create_profile, load_profile, update_profile


class TestCreateProfile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "profile.json")

    def test_create_profile_success(self):
        profile = create_profile("Alice", "alice@example.com", path=self.path)
        self.assertEqual(profile, {"name": "Alice", "email": "alice@example.com"})

    def test_create_profile_writes_file(self):
        create_profile("Alice", "alice@example.com", path=self.path)
        with open(self.path) as f:
            data = json.load(f)
        self.assertEqual(data, {"name": "Alice", "email": "alice@example.com"})

    def test_create_profile_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            create_profile("", "alice@example.com", path=self.path)
        self.assertIn("name must not be empty", str(ctx.exception))

    def test_create_profile_invalid_email_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            create_profile("Alice", "@bad", path=self.path)
        self.assertIn("email must be a valid email address", str(ctx.exception))

    def test_create_profile_invalid_email_no_at_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "notanemail", path=self.path)

    def test_create_profile_invalid_email_no_domain_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_profile("Alice", "alice@", path=self.path)


class TestLoadProfile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "profile.json")

    def test_load_profile_success(self):
        create_profile("Alice", "alice@example.com", path=self.path)
        profile = load_profile(path=self.path)
        self.assertEqual(profile, {"name": "Alice", "email": "alice@example.com"})

    def test_load_profile_nonexistent_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            load_profile("/nonexistent")

    def test_load_profile_missing_path_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            load_profile(path=os.path.join(self.tmpdir, "missing.json"))


class TestUpdateProfile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "profile.json")
        create_profile("Alice", "alice@example.com", path=self.path)

    def test_update_profile_name(self):
        profile = update_profile({"name": "Alice Smith"}, path=self.path)
        self.assertEqual(profile["name"], "Alice Smith")
        self.assertEqual(profile["email"], "alice@example.com")

    def test_update_profile_email(self):
        profile = update_profile({"email": "alice.smith@example.com"}, path=self.path)
        self.assertEqual(profile["email"], "alice.smith@example.com")

    def test_update_profile_persists(self):
        update_profile({"name": "Alice Smith"}, path=self.path)
        profile = load_profile(path=self.path)
        self.assertEqual(profile["name"], "Alice Smith")

    def test_update_profile_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            update_profile({"name": ""}, path=self.path)
        self.assertIn("name must not be empty", str(ctx.exception))

    def test_update_profile_invalid_email_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            update_profile({"email": "@bad"}, path=self.path)
        self.assertIn("email must be a valid email address", str(ctx.exception))

    def test_update_profile_nonexistent_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            update_profile({"name": "Bob"}, path="/nonexistent")


if __name__ == "__main__":
    unittest.main()
