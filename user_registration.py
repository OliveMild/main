#!/usr/bin/env python3
"""User registration module."""

import hashlib
import os
import re
import secrets


class ValidationError(Exception):
    """Raised when user input fails validation."""


class DuplicateUserError(Exception):
    """Raised when a user with the same username or email already exists."""


_SCRYPT_N = 16384
_SCRYPT_R = 8
_SCRYPT_P = 1


def _hash_password(password: str) -> str:
    """Return a salted scrypt hash of the given password.

    The returned string contains the hex-encoded salt and hash separated by
    ``:``, e.g. ``<salt_hex>:<hash_hex>``.  scrypt is a memory-hard key
    derivation function specifically designed for password storage.
    """
    salt = os.urandom(32)
    dk = hashlib.scrypt(password.encode(), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P)
    return salt.hex() + ":" + dk.hex()


def _verify_password(password: str, stored_hash: str) -> bool:
    """Return True if *password* matches the *stored_hash* produced by :func:`_hash_password`."""
    try:
        salt_hex, dk_hex = stored_hash.split(":", 1)
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.scrypt(password.encode(), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P)
    return secrets.compare_digest(dk.hex(), dk_hex)


def _validate_username(username: str) -> None:
    if not username.strip():
        raise ValidationError("Username must not be empty.")
    if len(username) < 3 or len(username) > 50:
        raise ValidationError("Username must be between 3 and 50 characters.")
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        raise ValidationError(
            "Username may only contain letters, digits, and underscores."
        )


def _validate_email(email: str) -> None:
    if not email.strip():
        raise ValidationError("Email must not be empty.")
    # Require exactly one '@', a non-empty local part, and a non-empty domain.
    if email.count("@") != 1:
        raise ValidationError("Email address is not valid.")
    local, domain = email.split("@", 1)
    # Local part must be non-empty and free of whitespace.
    if not local or re.search(r"\s", local):
        raise ValidationError("Email address is not valid.")
    # Domain must be non-empty, contain at least one dot, have no whitespace,
    # no consecutive dots, and must not start or end with a dot.
    if (
        not domain
        or re.search(r"\s", domain)
        or "." not in domain
        or ".." in domain
        or domain.startswith(".")
        or domain.endswith(".")
    ):
        raise ValidationError("Email address is not valid.")


_PASSWORD_MAX_LENGTH = 128


def _validate_password(password: str) -> None:
    if not password:
        raise ValidationError("Password must not be empty.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if len(password) > _PASSWORD_MAX_LENGTH:
        raise ValidationError(
            f"Password must not exceed {_PASSWORD_MAX_LENGTH} characters."
        )
    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must contain at least one letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit.")


class User:
    """Represents a registered user."""

    def __init__(self, username: str, email: str, password_hash: str) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password: str) -> bool:
        """Return True if the given password matches the stored hash."""
        return _verify_password(password, self.password_hash)

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, email={self.email!r})"


class UserRegistry:
    """Manages a collection of registered users."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._emails: dict[str, User] = {}

    def register(self, username: str, email: str, password: str) -> User:
        """Register a new user and return the created User object.

        Raises:
            ValidationError: If any input fails validation.
            DuplicateUserError: If the username or email is already taken.
        """
        _validate_username(username)
        _validate_email(email)
        _validate_password(password)

        lower_username = username.lower()
        lower_email = email.lower()

        if lower_username in self._users:
            raise DuplicateUserError(f"Username '{username}' is already taken.")
        if lower_email in self._emails:
            raise DuplicateUserError(f"Email '{email}' is already registered.")

        user = User(username, email, _hash_password(password))
        self._users[lower_username] = user
        self._emails[lower_email] = user
        return user

    def get_user(self, username: str) -> "User | None":
        """Return the User with the given username, or None if not found."""
        return self._users.get(username.lower())

    def __len__(self) -> int:
        return len(self._users)
