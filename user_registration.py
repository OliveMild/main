#!/usr/bin/env python3
"""User registration module."""

from email_validator import is_valid_email


def register_user(username: object, email: object) -> dict:
    """Register a new user with the given username and email.

    Returns a dict with keys:
      - 'success' (bool)
      - 'error'   (str | None) – human-readable message when not successful
      - 'username' and 'email' (str) – present only on success
    """
    if not isinstance(username, str) or not username.strip():
        return {"success": False, "error": "Username is required."}
    if not is_valid_email(email):
        return {"success": False, "error": "Invalid email address."}
    return {"success": True, "error": None,
            "username": username.strip(), "email": email.strip()}
