#!/usr/bin/env python3
"""User registration module with email validation."""

import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_%+\-]+(\.[a-zA-Z0-9_%+\-]+)*"
    r"@"
    r"[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$"
)


def validate_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise."""
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email:
        return False
    return bool(_EMAIL_REGEX.match(email))


def register_user(username: str, email: str) -> dict:
    """Register a user with the given username and email.

    Returns a dict with keys:
      - 'success' (bool)
      - 'error'   (str | None) – human-readable error message when not successful
    """
    if not isinstance(username, str) or not username.strip():
        return {"success": False, "error": "Username is required."}
    if not validate_email(email):
        return {"success": False, "error": "Invalid email address."}
    return {"success": True, "error": None}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: registration.py <username> <email>")
        sys.exit(1)
    result = register_user(sys.argv[1], sys.argv[2])
    if result["success"]:
        print(f"User '{sys.argv[1]}' registered successfully.")
    else:
        print(f"Registration failed: {result['error']}")
        sys.exit(1)
