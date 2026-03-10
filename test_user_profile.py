#!/usr/bin/env python3
"""Tests for user_profile module."""

import unittest

from user_profile import (
    BIO_MAX_LENGTH,
    DISPLAY_NAME_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    DuplicateUsernameError,
    InvalidBioError,
    InvalidDisplayNameError,
    InvalidEmailError,
    InvalidUsernameError,
    ProfileNotFoundError,
    ProfileStore,
    UserProfile,
    UserProfileError,
)


class TestExceptionHierarchy(unittest.TestCase):
    def test_invalid_username_is_user_profile_error(self):
        self.assertTrue(issubclass(InvalidUsernameError, UserProfileError))

    def test_invalid_email_is_user_profile_error(self):
        self.assertTrue(issubclass(InvalidEmailError, UserProfileError))

    def test_invalid_display_name_is_user_profile_error(self):
        self.assertTrue(issubclass(InvalidDisplayNameError, UserProfileError))

    def test_invalid_bio_is_user_profile_error(self):
        self.assertTrue(issubclass(InvalidBioError, UserProfileError))

    def test_profile_not_found_is_user_profile_error(self):
        self.assertTrue(issubclass(ProfileNotFoundError, UserProfileError))

    def test_duplicate_username_is_user_profile_error(self):
        self.assertTrue(issubclass(DuplicateUsernameError, UserProfileError))


class TestUserProfileConstruction(unittest.TestCase):
    def test_valid_minimal_construction(self):
        p = UserProfile(username="alice", email="alice@example.com")
        self.assertEqual(p.username, "alice")
        self.assertEqual(p.email, "alice@example.com")
        self.assertEqual(p.display_name, "")
        self.assertEqual(p.bio, "")

    def test_valid_full_construction(self):
        p = UserProfile(
            username="bob_99",
            email="bob@example.com",
            display_name="Bob Smith",
            bio="Hello there",
        )
        self.assertEqual(p.username, "bob_99")
        self.assertEqual(p.display_name, "Bob Smith")
        self.assertEqual(p.bio, "Hello there")

    def test_created_at_is_set(self):
        p = UserProfile(username="carol", email="carol@example.com")
        self.assertIsNotNone(p.created_at)

    def test_updated_at_equals_created_at_initially(self):
        p = UserProfile(username="dave", email="dave@example.com")
        self.assertEqual(p.created_at, p.updated_at)

    def test_username_min_length(self):
        p = UserProfile(username="a" * USERNAME_MIN_LENGTH, email="x@x.com")
        self.assertEqual(len(p.username), USERNAME_MIN_LENGTH)

    def test_username_max_length(self):
        p = UserProfile(username="a" * USERNAME_MAX_LENGTH, email="x@x.com")
        self.assertEqual(len(p.username), USERNAME_MAX_LENGTH)


class TestUsernameValidation(unittest.TestCase):
    def test_empty_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username="", email="x@x.com")

    def test_none_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username=None, email="x@x.com")

    def test_too_short_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username="ab", email="x@x.com")

    def test_too_long_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username="a" * (USERNAME_MAX_LENGTH + 1), email="x@x.com")

    def test_username_with_spaces_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username="bad user", email="x@x.com")

    def test_username_with_hyphen_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username="bad-user", email="x@x.com")

    def test_username_integer_raises(self):
        with self.assertRaises(InvalidUsernameError):
            UserProfile(username=123, email="x@x.com")


class TestEmailValidation(unittest.TestCase):
    def test_empty_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email="")

    def test_none_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email=None)

    def test_missing_at_sign_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email="notanemail")

    def test_missing_domain_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email="alice@")

    def test_email_with_spaces_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email="alice @example.com")

    def test_integer_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            UserProfile(username="alice", email=42)


class TestDisplayNameValidation(unittest.TestCase):
    def test_too_long_display_name_raises(self):
        with self.assertRaises(InvalidDisplayNameError):
            UserProfile(
                username="alice",
                email="alice@example.com",
                display_name="x" * (DISPLAY_NAME_MAX_LENGTH + 1),
            )

    def test_max_length_display_name_is_valid(self):
        p = UserProfile(
            username="alice",
            email="alice@example.com",
            display_name="x" * DISPLAY_NAME_MAX_LENGTH,
        )
        self.assertEqual(len(p.display_name), DISPLAY_NAME_MAX_LENGTH)

    def test_non_string_display_name_raises(self):
        with self.assertRaises(InvalidDisplayNameError):
            UserProfile(username="alice", email="alice@example.com", display_name=123)


class TestBioValidation(unittest.TestCase):
    def test_too_long_bio_raises(self):
        with self.assertRaises(InvalidBioError):
            UserProfile(
                username="alice",
                email="alice@example.com",
                bio="x" * (BIO_MAX_LENGTH + 1),
            )

    def test_max_length_bio_is_valid(self):
        p = UserProfile(
            username="alice",
            email="alice@example.com",
            bio="x" * BIO_MAX_LENGTH,
        )
        self.assertEqual(len(p.bio), BIO_MAX_LENGTH)

    def test_non_string_bio_raises(self):
        with self.assertRaises(InvalidBioError):
            UserProfile(username="alice", email="alice@example.com", bio=["list"])


class TestUserProfileSetters(unittest.TestCase):
    def setUp(self):
        self.profile = UserProfile(
            username="alice",
            email="alice@example.com",
            display_name="Alice",
            bio="Hello",
        )

    def test_set_valid_email(self):
        self.profile.email = "newalice@example.com"
        self.assertEqual(self.profile.email, "newalice@example.com")

    def test_set_invalid_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            self.profile.email = "notvalid"

    def test_set_valid_display_name(self):
        self.profile.display_name = "Alice Smith"
        self.assertEqual(self.profile.display_name, "Alice Smith")

    def test_set_invalid_display_name_raises(self):
        with self.assertRaises(InvalidDisplayNameError):
            self.profile.display_name = "x" * (DISPLAY_NAME_MAX_LENGTH + 1)

    def test_set_valid_bio(self):
        self.profile.bio = "Updated bio"
        self.assertEqual(self.profile.bio, "Updated bio")

    def test_set_invalid_bio_raises(self):
        with self.assertRaises(InvalidBioError):
            self.profile.bio = "x" * (BIO_MAX_LENGTH + 1)

    def test_updated_at_changes_after_setter(self):
        before = self.profile.updated_at
        self.profile.bio = "New bio"
        self.assertGreaterEqual(self.profile.updated_at, before)

    def test_username_is_immutable(self):
        with self.assertRaises(AttributeError):
            self.profile.username = "other"


class TestUserProfileToDict(unittest.TestCase):
    def test_to_dict_keys(self):
        p = UserProfile(username="alice", email="alice@example.com")
        d = p.to_dict()
        for key in ("username", "email", "display_name", "bio", "created_at", "updated_at"):
            self.assertIn(key, d)

    def test_to_dict_values(self):
        p = UserProfile(username="bob", email="bob@example.com", display_name="Bob")
        d = p.to_dict()
        self.assertEqual(d["username"], "bob")
        self.assertEqual(d["email"], "bob@example.com")
        self.assertEqual(d["display_name"], "Bob")


class TestProfileStore(unittest.TestCase):
    def setUp(self):
        self.store = ProfileStore()

    def test_empty_store_len_is_zero(self):
        self.assertEqual(len(self.store), 0)

    def test_create_returns_profile(self):
        p = self.store.create("alice", "alice@example.com")
        self.assertIsInstance(p, UserProfile)

    def test_create_increases_len(self):
        self.store.create("alice", "alice@example.com")
        self.assertEqual(len(self.store), 1)

    def test_get_returns_correct_profile(self):
        self.store.create("alice", "alice@example.com")
        p = self.store.get("alice")
        self.assertEqual(p.username, "alice")

    def test_get_nonexistent_raises(self):
        with self.assertRaises(ProfileNotFoundError):
            self.store.get("nobody")

    def test_get_invalid_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            self.store.get("")

    def test_duplicate_username_raises(self):
        self.store.create("alice", "alice@example.com")
        with self.assertRaises(DuplicateUsernameError):
            self.store.create("alice", "other@example.com")

    def test_update_email(self):
        self.store.create("alice", "alice@example.com")
        p = self.store.update("alice", email="new@example.com")
        self.assertEqual(p.email, "new@example.com")

    def test_update_display_name(self):
        self.store.create("alice", "alice@example.com")
        p = self.store.update("alice", display_name="Alice Smith")
        self.assertEqual(p.display_name, "Alice Smith")

    def test_update_bio(self):
        self.store.create("alice", "alice@example.com")
        p = self.store.update("alice", bio="New bio")
        self.assertEqual(p.bio, "New bio")

    def test_update_nonexistent_raises(self):
        with self.assertRaises(ProfileNotFoundError):
            self.store.update("nobody", bio="test")

    def test_update_invalid_email_raises(self):
        self.store.create("alice", "alice@example.com")
        with self.assertRaises(InvalidEmailError):
            self.store.update("alice", email="bad")

    def test_delete_removes_profile(self):
        self.store.create("alice", "alice@example.com")
        self.store.delete("alice")
        self.assertEqual(len(self.store), 0)

    def test_delete_nonexistent_raises(self):
        with self.assertRaises(ProfileNotFoundError):
            self.store.delete("nobody")

    def test_get_all_returns_all_profiles(self):
        self.store.create("alice", "alice@example.com")
        self.store.create("bob", "bob@example.com")
        profiles = self.store.get_all()
        self.assertEqual(len(profiles), 2)

    def test_get_all_is_copy(self):
        self.store.create("alice", "alice@example.com")
        profiles = self.store.get_all()
        profiles.clear()
        self.assertEqual(len(self.store), 1)

    def test_create_with_invalid_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            self.store.create("alice", "notanemail")

    def test_create_with_invalid_username_raises(self):
        with self.assertRaises(InvalidUsernameError):
            self.store.create("ab", "alice@example.com")


if __name__ == "__main__":
    unittest.main()
