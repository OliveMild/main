#!/usr/bin/env python3
from email_validator import is_valid_email


def register_user(username: str, email: str) -> dict:
    """Register a new user.

    Returns a dict with 'success' bool and an optional 'error' message.
    """
    if not username or not username.strip():
        return {"success": False, "error": "Username is required."}

    if not is_valid_email(email):
        return {"success": False, "error": "Invalid email address."}

    return {"success": True, "username": username.strip(), "email": email}
