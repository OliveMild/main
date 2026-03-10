#!/usr/bin/env python3
"""User registration module."""

from email_validator import is_valid_email


def register_user(username, email, password):
    """Register a new user with basic validation.

    Args:
        username: The desired username.
        email: The user's email address.
        password: The user's password (minimum 8 characters).

    Returns:
        A dict with:
          - 'success' (bool): whether registration succeeded.
          - 'message' (str): a human-readable result message.
    """
    if not username or not isinstance(username, str) or not username.strip():
        return {'success': False, 'message': 'Username is required.'}

    username = username.strip()

    if not is_valid_email(email):
        return {'success': False, 'message': 'Invalid email address.'}

    if not isinstance(password, str) or len(password) < 8:
        return {'success': False, 'message': 'Password must be at least 8 characters.'}

    return {
        'success': True,
        'message': f"User '{username}' registered successfully.",
    }


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 4:
        print('Usage: user_registration.py <username> <email> <password>')
        sys.exit(1)

    result = register_user(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result['message'])
    sys.exit(0 if result['success'] else 1)
