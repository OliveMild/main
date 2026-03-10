#!/usr/bin/env python3
"""User registration module with validated input and secure password hashing."""

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
_PASSWORD_MAX_LENGTH = 128


def _hash_password(password: str) -> str:
    """Return a salted scrypt hash of *password*.

    The returned string is ``<salt_hex>:<hash_hex>`` where the salt is a
    random 32-byte value.  scrypt is a memory-hard KDF designed for password
    storage.
    """
    salt = os.urandom(32)
    dk = hashlib.scrypt(
        password.encode(), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P
    )
    return salt.hex() + ":" + dk.hex()


def _verify_password(password: str, stored_hash: str) -> bool:
    """Return True if *password* matches *stored_hash* from :func:`_hash_password`."""
    try:
        salt_hex, dk_hex = stored_hash.split(":", 1)
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.scrypt(
        password.encode(), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P
    )
    return secrets.compare_digest(dk.hex(), dk_hex)


def _validate_username(username: str) -> None:
    """Raise :class:`ValidationError` if *username* is invalid."""
    if not username or not username.strip():
        raise ValidationError("Username must not be empty.")
    if len(username) < 3 or len(username) > 50:
        raise ValidationError("Username must be between 3 and 50 characters.")
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        raise ValidationError(
            "Username may only contain letters, digits, and underscores."
        )


def _validate_email(email: str) -> None:
    """Raise :class:`ValidationError` if *email* is not a valid email address.

    Rules applied:
    - Must not be empty or whitespace-only.
    - Must contain exactly one ``@`` character.
    - The local part (before ``@``) must be non-empty and contain no whitespace.
    - The domain part (after ``@``) must be non-empty, contain at least one
      dot, have no whitespace, no consecutive dots, and must not start or end
      with a dot.
    """
    if not email or not email.strip():
        raise ValidationError("Email must not be empty.")
    if email.count("@") != 1:
        raise ValidationError("Email address is not valid.")
    local, domain = email.split("@", 1)
    if not local or re.search(r"\s", local):
        raise ValidationError("Email address is not valid.")
    if (
        not domain
        or re.search(r"\s", domain)
        or "." not in domain
        or ".." in domain
        or domain.startswith(".")
        or domain.endswith(".")
    ):
        raise ValidationError("Email address is not valid.")


def _validate_password(password: str) -> None:
    """Raise :class:`ValidationError` if *password* does not meet requirements."""
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
        """Return True if *password* matches the stored hash."""
        return _verify_password(password, self.password_hash)

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, email={self.email!r})"


class UserRegistry:
    """In-memory registry of registered users."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._emails: dict[str, User] = {}

    def register(self, username: str, email: str, password: str) -> User:
        """Register a new user and return the created :class:`User`.

        Args:
            username: Desired username (3–50 chars, ``[A-Za-z0-9_]`` only).
            email: User's email address.
            password: Plaintext password (8–128 chars, ≥1 letter, ≥1 digit).

        Returns:
            The newly created :class:`User` object.

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
        # Both dicts hold a reference to the same User object for O(1) lookup
        # by either username or email without duplicating data.
        self._users[lower_username] = user
        self._emails[lower_email] = user
        return user

    def get_user(self, username: str) -> "User | None":
        """Return the :class:`User` with *username* (case-insensitive), or None."""
        return self._users.get(username.lower())

    def __len__(self) -> int:
        return len(self._users)
