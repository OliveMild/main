#!/usr/bin/env python3
"""Tests for the user registration module."""

import pytest

from user_registration import (
    DuplicateUserError,
    User,
    UserRegistry,
    ValidationError,
    _hash_password,
    _verify_password,
)


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

class TestHashPassword:
    def test_different_passwords_give_different_hashes(self):
        h1 = _hash_password("Secret1")
        h2 = _hash_password("Secret2")
        assert h1 != h2

    def test_same_password_verifies_correctly(self):
        h = _hash_password("Secret1")
        assert _verify_password("Secret1", h) is True

    def test_wrong_password_does_not_verify(self):
        h = _hash_password("Secret1")
        assert _verify_password("Secret2", h) is False

    def test_hash_includes_salt_and_dk(self):
        h = _hash_password("Secret1")
        assert ":" in h

    def test_two_hashes_of_same_password_differ_due_to_salt(self):
        # scrypt uses a random salt, so the stored hash should differ each time
        h1 = _hash_password("Secret1")
        h2 = _hash_password("Secret1")
        assert h1 != h2


# ---------------------------------------------------------------------------
# User.check_password
# ---------------------------------------------------------------------------

class TestUserCheckPassword:
    def _make_user(self, password: str) -> User:
        return User("alice", "alice@example.com", _hash_password(password))

    def test_correct_password_returns_true(self):
        user = self._make_user("P@ssword1")
        assert user.check_password("P@ssword1") is True

    def test_wrong_password_returns_false(self):
        user = self._make_user("P@ssword1")
        assert user.check_password("WrongPass1") is False


# ---------------------------------------------------------------------------
# UserRegistry.register – happy path
# ---------------------------------------------------------------------------

class TestUserRegistryRegister:
    def setup_method(self):
        self.registry = UserRegistry()

    def test_register_returns_user(self):
        user = self.registry.register("alice", "alice@example.com", "Password1")
        assert isinstance(user, User)

    def test_registered_user_attributes(self):
        user = self.registry.register("alice", "alice@example.com", "Password1")
        assert user.username == "alice"
        assert user.email == "alice@example.com"

    def test_password_is_hashed(self):
        user = self.registry.register("alice", "alice@example.com", "Password1")
        assert ":" in user.password_hash  # salt:hash format

    def test_check_password_works_after_registration(self):
        user = self.registry.register("alice", "alice@example.com", "Password1")
        assert user.check_password("Password1") is True

    def test_registry_length_increases(self):
        assert len(self.registry) == 0
        self.registry.register("alice", "alice@example.com", "Password1")
        assert len(self.registry) == 1
        self.registry.register("bob", "bob@example.com", "Password2")
        assert len(self.registry) == 2

    def test_get_user_returns_registered_user(self):
        self.registry.register("alice", "alice@example.com", "Password1")
        user = self.registry.get_user("alice")
        assert user is not None
        assert user.username == "alice"

    def test_get_user_case_insensitive(self):
        self.registry.register("alice", "alice@example.com", "Password1")
        assert self.registry.get_user("ALICE") is not None

    def test_get_user_unknown_returns_none(self):
        assert self.registry.get_user("nobody") is None


# ---------------------------------------------------------------------------
# UserRegistry.register – duplicate detection
# ---------------------------------------------------------------------------

class TestUserRegistryDuplicates:
    def setup_method(self):
        self.registry = UserRegistry()
        self.registry.register("alice", "alice@example.com", "Password1")

    def test_duplicate_username_raises(self):
        with pytest.raises(DuplicateUserError):
            self.registry.register("alice", "other@example.com", "Password1")

    def test_duplicate_username_case_insensitive(self):
        with pytest.raises(DuplicateUserError):
            self.registry.register("ALICE", "other@example.com", "Password1")

    def test_duplicate_email_raises(self):
        with pytest.raises(DuplicateUserError):
            self.registry.register("bob", "alice@example.com", "Password1")

    def test_duplicate_email_case_insensitive(self):
        with pytest.raises(DuplicateUserError):
            self.registry.register("bob", "ALICE@EXAMPLE.COM", "Password1")


# ---------------------------------------------------------------------------
# Input validation – username
# ---------------------------------------------------------------------------

class TestUsernameValidation:
    def setup_method(self):
        self.registry = UserRegistry()

    def test_empty_username_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("", "a@example.com", "Password1")

    def test_whitespace_username_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("   ", "a@example.com", "Password1")

    def test_short_username_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("ab", "a@example.com", "Password1")

    def test_long_username_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("a" * 51, "a@example.com", "Password1")

    def test_special_chars_in_username_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("ali ce", "a@example.com", "Password1")

    def test_valid_username_with_underscores(self):
        user = self.registry.register("alice_99", "a@example.com", "Password1")
        assert user.username == "alice_99"


# ---------------------------------------------------------------------------
# Input validation – email
# ---------------------------------------------------------------------------

class TestEmailValidation:
    def setup_method(self):
        self.registry = UserRegistry()

    def test_empty_email_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "", "Password1")

    def test_missing_at_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "notanemail", "Password1")

    def test_missing_domain_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@", "Password1")

    def test_domain_without_dot_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@nodot", "Password1")

    def test_domain_with_consecutive_dots_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@exam..ple.com", "Password1")

    def test_domain_starting_with_dot_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@.example.com", "Password1")

    def test_domain_ending_with_dot_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com.", "Password1")

    def test_multiple_at_signs_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "a@b@example.com", "Password1")

    def test_valid_email_accepted(self):
        user = self.registry.register("alice", "alice@example.com", "Password1")
        assert user.email == "alice@example.com"


# ---------------------------------------------------------------------------
# Input validation – password
# ---------------------------------------------------------------------------

class TestPasswordValidation:
    def setup_method(self):
        self.registry = UserRegistry()

    def test_empty_password_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com", "")

    def test_short_password_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com", "Abc1")

    def test_no_letter_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com", "12345678")

    def test_no_digit_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com", "abcdefgh")

    def test_too_long_password_raises(self):
        with pytest.raises(ValidationError):
            self.registry.register("alice", "alice@example.com", "Password1" + "x" * 120)
