#!/usr/bin/env python3
"""Tests for user_registration.py, focusing on email validation."""

import pytest

from user_registration import (
    DuplicateUserError,
    User,
    UserRegistry,
    ValidationError,
    _validate_email,
    _validate_password,
    _validate_username,
)


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------


class TestValidateEmail:
    def test_valid_simple(self):
        _validate_email("user@example.com")

    def test_valid_subdomain(self):
        _validate_email("user@mail.example.com")

    def test_valid_plus_addressing(self):
        _validate_email("user+tag@example.com")

    def test_valid_dots_in_local(self):
        _validate_email("first.last@example.com")

    def test_valid_numeric_local(self):
        _validate_email("123@example.com")

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("   ")

    def test_missing_at_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("userexample.com")

    def test_multiple_at_signs_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@@example.com")

    def test_empty_local_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("@example.com")

    def test_whitespace_in_local_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("us er@example.com")

    def test_empty_domain_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@")

    def test_domain_no_dot_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@localhost")

    def test_domain_starts_with_dot_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@.example.com")

    def test_domain_ends_with_dot_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@example.com.")

    def test_domain_consecutive_dots_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@exam..ple.com")

    def test_whitespace_in_domain_raises(self):
        with pytest.raises(ValidationError):
            _validate_email("user@exam ple.com")


# ---------------------------------------------------------------------------
# Username validation
# ---------------------------------------------------------------------------


class TestValidateUsername:
    def test_valid(self):
        _validate_username("alice")

    def test_valid_with_digits_and_underscore(self):
        _validate_username("alice_123")

    def test_empty_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("")

    def test_too_short_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("ab")

    def test_too_long_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("a" * 51)

    def test_invalid_chars_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("alice!")


# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------


class TestValidatePassword:
    def test_valid(self):
        _validate_password("Secret42")

    def test_empty_raises(self):
        with pytest.raises(ValidationError):
            _validate_password("")

    def test_too_short_raises(self):
        with pytest.raises(ValidationError):
            _validate_password("Abc1")

    def test_too_long_raises(self):
        with pytest.raises(ValidationError):
            _validate_password("A1" + "a" * 127)

    def test_no_letter_raises(self):
        with pytest.raises(ValidationError):
            _validate_password("12345678")

    def test_no_digit_raises(self):
        with pytest.raises(ValidationError):
            _validate_password("abcdefgh")


# ---------------------------------------------------------------------------
# User and UserRegistry
# ---------------------------------------------------------------------------


class TestUserRegistry:
    def setup_method(self):
        self.registry = UserRegistry()

    def test_register_returns_user(self):
        user = self.registry.register("alice", "alice@example.com", "Secret42")
        assert isinstance(user, User)
        assert user.username == "alice"
        assert user.email == "alice@example.com"

    def test_password_check_correct(self):
        user = self.registry.register("bob", "bob@example.com", "Pass1234")
        assert user.check_password("Pass1234") is True

    def test_password_check_wrong(self):
        user = self.registry.register("carol", "carol@example.com", "Pass1234")
        assert user.check_password("wrong") is False

    def test_duplicate_username_raises(self):
        self.registry.register("dave", "dave@example.com", "Pass1234")
        with pytest.raises(DuplicateUserError):
            self.registry.register("dave", "dave2@example.com", "Pass1234")

    def test_duplicate_username_case_insensitive(self):
        self.registry.register("Eve", "eve@example.com", "Pass1234")
        with pytest.raises(DuplicateUserError):
            self.registry.register("eve", "eve2@example.com", "Pass1234")

    def test_duplicate_email_raises(self):
        self.registry.register("frank", "frank@example.com", "Pass1234")
        with pytest.raises(DuplicateUserError):
            self.registry.register("frank2", "frank@example.com", "Pass1234")

    def test_duplicate_email_case_insensitive(self):
        self.registry.register("grace", "Grace@Example.COM", "Pass1234")
        with pytest.raises(DuplicateUserError):
            self.registry.register("grace2", "grace@example.com", "Pass1234")

    def test_get_user_found(self):
        self.registry.register("heidi", "heidi@example.com", "Pass1234")
        user = self.registry.get_user("heidi")
        assert user is not None
        assert user.username == "heidi"

    def test_get_user_case_insensitive(self):
        self.registry.register("ivan", "ivan@example.com", "Pass1234")
        assert self.registry.get_user("IVAN") is not None

    def test_get_user_not_found(self):
        assert self.registry.get_user("nobody") is None

    def test_len(self):
        assert len(self.registry) == 0
        self.registry.register("judy", "judy@example.com", "Pass1234")
        assert len(self.registry) == 1

    def test_invalid_email_raises_validation_error(self):
        with pytest.raises(ValidationError):
            self.registry.register("mallory", "not-an-email", "Pass1234")

    def test_repr(self):
        user = self.registry.register("nick", "nick@example.com", "Pass1234")
        assert "nick" in repr(user)
        assert "nick@example.com" in repr(user)
