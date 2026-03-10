#!/usr/bin/env python3
"""User registration module with email validation."""

import re

_EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9]'                  # local part must start with alphanumeric
    r'(?:[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]'  # allowed chars in local part
    r'|\.(?!\.))*'                   # dots allowed but not consecutive
    r'(?<!\.)@'                      # local part must not end with a dot
    r'(?:[a-zA-Z0-9]'               # domain label start (one or more required)
    r'(?:[a-zA-Z0-9-]*[a-zA-Z0-9])?'  # domain label rest
    r'\.)+'                          # at least one dot required before TLD
    r'[a-zA-Z]{2,}$'                # top-level domain (at least 2 chars)
)


def validate_email(email):
    """Return True if *email* is a valid email address, False otherwise.

    Validation rules:
    - Must be a non-empty string
    - Must contain exactly one '@'
    - Local part must not start or end with a dot
    - Local part must not contain consecutive dots
    - Domain must contain at least one dot
    - TLD must be at least two alphabetic characters
    - No whitespace allowed anywhere
    """
    if not isinstance(email, str):
        return False
    if ' ' in email or '\t' in email:
        return False
    if email.count('@') != 1:
        return False
    return bool(_EMAIL_REGEX.match(email))


def register_user(username, email, password):
    """Register a new user after validating inputs.

    Parameters
    ----------
    username : str
        The desired username (must be non-empty after stripping whitespace).
    email : str
        The user's email address (must pass :func:`validate_email`).
    password : str
        The user's password (must be a string of at least 8 non-whitespace
        characters).

    Returns
    -------
    dict
        ``{'success': True, 'message': "User '<username>' registered successfully."}``
        on success, or ``{'success': False, 'message': '<reason>'}`` on failure.
    """
    if not isinstance(username, str) or not username.strip():
        return {'success': False, 'message': 'Username is required.'}
    if not validate_email(email):
        return {'success': False, 'message': 'Invalid email address.'}
    if not isinstance(password, str) or len(re.sub(r'\s', '', password)) < 8:
        return {'success': False, 'message': 'Password must be at least 8 non-whitespace characters.'}
    return {'success': True, 'message': f"User '{username.strip()}' registered successfully."}
