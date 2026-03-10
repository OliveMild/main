#!/usr/bin/env python3
"""User registration module with email validation."""

import re

_EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$')


def validate_email(email):
    """Validate an email address.

    Args:
        email: The email address string to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    if len(email) > 320:
        return False
    if ' ' in email:
        return False
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if '..' in local or '..' in domain:
        return False
    return bool(_EMAIL_PATTERN.match(email))


def register_user(username, email, password):
    """Register a new user.

    Args:
        username: The desired username.
        email: The user's email address.
        password: The user's password.

    Returns:
        A dict with 'success' (bool) and 'message' (str).
    """
    if not username or not isinstance(username, str) or not username.strip():
        return {'success': False, 'message': 'Username is required.'}

    username = username.strip()

    if not validate_email(email):
        return {'success': False, 'message': 'Invalid email address.'}

    if not isinstance(password, str) or not password.strip() or len(password.strip()) < 8:
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
