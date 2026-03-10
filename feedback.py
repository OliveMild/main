#!/usr/bin/env python3
"""User feedback module with persistent JSON storage."""

import json
import os
from datetime import datetime, timezone

DEFAULT_FILEPATH = "feedback.json"


def submit_feedback(rating, comment="", filepath=DEFAULT_FILEPATH):
    """Submit feedback with a 1-5 rating and optional comment.

    Args:
        rating: Integer rating between 1 and 5 (inclusive).
        comment: Optional string comment (default "").
        filepath: Path to the JSON storage file.

    Raises:
        TypeError: If rating is not an integer (booleans are rejected).
        ValueError: If rating is not between 1 and 5.
    """
    if isinstance(rating, bool) or not isinstance(rating, int):
        raise TypeError("rating must be an integer")
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")

    entries = load_feedback(filepath)
    entries.append({
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def load_feedback(filepath=DEFAULT_FILEPATH):
    """Load all feedback entries from the JSON store.

    Returns an empty list if the file is missing or corrupt.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def get_average_rating(filepath=DEFAULT_FILEPATH):
    """Return the average rating across all stored entries.

    Returns 0.0 if there are no entries.
    """
    entries = load_feedback(filepath)
    if not entries:
        return 0.0
    return sum(e["rating"] for e in entries) / len(entries)
