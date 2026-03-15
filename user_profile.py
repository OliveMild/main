#!/usr/bin/env python3
"""User profile module."""

_ALLOWED_FIELDS = {"display_name", "bio", "location", "website"}
_MAX_LENGTHS = {
    "display_name": 100,
    "bio": 300,
    "location": 100,
    "website": 200,
}


def get_profile(user_id: object, profiles: dict) -> dict:
    """Return the profile for the given user_id from the profiles store.

    Returns a dict with keys:
      - 'success' (bool)
      - 'error'   (str | None) – human-readable message when not successful
      - 'profile' (dict | None) – the profile data on success
    """
    if not isinstance(user_id, str) or not user_id.strip():
        return {"success": False, "error": "User ID is required.", "profile": None}
    if not isinstance(profiles, dict):
        return {"success": False, "error": "Invalid profiles store.", "profile": None}
    user_id = user_id.strip()
    if user_id not in profiles:
        return {"success": False, "error": "User profile not found.", "profile": None}
    return {"success": True, "error": None, "profile": dict(profiles[user_id])}


def update_profile(user_id: object, updates: object, profiles: dict) -> dict:
    """Update fields in the user profile for the given user_id.

    Only fields in _ALLOWED_FIELDS are accepted; unknown fields are rejected.
    Each field value must be a string and must not exceed its maximum length.

    Returns a dict with keys:
      - 'success' (bool)
      - 'error'   (str | None) – human-readable message when not successful
      - 'profile' (dict | None) – the updated profile on success
    """
    if not isinstance(user_id, str) or not user_id.strip():
        return {"success": False, "error": "User ID is required.", "profile": None}
    if not isinstance(updates, dict):
        return {"success": False, "error": "Updates must be a dictionary.", "profile": None}
    if not isinstance(profiles, dict):
        return {"success": False, "error": "Invalid profiles store.", "profile": None}
    user_id = user_id.strip()
    if user_id not in profiles:
        return {"success": False, "error": "User profile not found.", "profile": None}

    unknown = set(updates.keys()) - _ALLOWED_FIELDS
    if unknown:
        return {"success": False, "error": "Unknown profile field(s) provided.", "profile": None}

    for field, value in updates.items():
        if not isinstance(value, str):
            return {
                "success": False,
                "error": f"Field '{field}' must be a string.",
                "profile": None,
            }
        if len(value) > _MAX_LENGTHS[field]:
            return {
                "success": False,
                "error": f"Field '{field}' exceeds maximum allowed length.",
                "profile": None,
            }

    profiles[user_id].update({k: v.strip() for k, v in updates.items()})
    return {"success": True, "error": None, "profile": dict(profiles[user_id])}


def create_profile(user_id: object, profiles: dict) -> dict:
    """Create a new empty profile for the given user_id.

    Returns a dict with keys:
      - 'success' (bool)
      - 'error'   (str | None) – human-readable message when not successful
      - 'profile' (dict | None) – the new profile on success
    """
    if not isinstance(user_id, str) or not user_id.strip():
        return {"success": False, "error": "User ID is required.", "profile": None}
    if not isinstance(profiles, dict):
        return {"success": False, "error": "Invalid profiles store.", "profile": None}
    user_id = user_id.strip()
    if user_id in profiles:
        return {"success": False, "error": "User profile already exists.", "profile": None}
    profiles[user_id] = {field: "" for field in _ALLOWED_FIELDS}
    return {"success": True, "error": None, "profile": dict(profiles[user_id])}
