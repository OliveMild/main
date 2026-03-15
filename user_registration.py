from email_validator import is_valid_email


def register_user(username: object, email: object) -> dict:
    """Register a new user after validating *username* and *email*.

    Returns a dict with the keys:
    - ``success`` (bool)
    - ``error``   (str or None)
    - ``username``(str, only when success is True)
    - ``email``   (str, only when success is True)

    Error messages never echo back the raw input values.
    """
    if not isinstance(username, str) or not username.strip():
        return {"success": False, "error": "Username is required."}

    if not isinstance(email, str) or not email.strip():
        return {"success": False, "error": "Email is required."}

    clean_email = email.strip()
    if not is_valid_email(clean_email):
        return {"success": False, "error": "Invalid email address."}

    return {
        "success": True,
        "error": None,
        "username": username.strip(),
        "email": clean_email,
    }
