#!/usr/bin/env python3
"""User feedback module for collecting, persisting, and summarizing ratings."""

import json
import os
from datetime import datetime, timezone

DEFAULT_FILEPATH = "feedback.json"


def submit_feedback(rating, comment="", filepath=DEFAULT_FILEPATH):
    """Validate and persist a user rating (1–5) with an optional comment.

    Args:
        rating: An integer between 1 and 5 (inclusive). Booleans are rejected.
        comment: An optional string comment (default "").
        filepath: Path to the JSON file used for storage.

    Raises:
        ValueError: If rating is not an integer in the range 1–5.
    """
    if isinstance(rating, bool) or not isinstance(rating, int):
        raise ValueError("rating must be an integer")
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")

    entry = {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    entries = _load(filepath)
    entries.append(entry)
    _save(filepath, entries)


def get_all_feedback(filepath=DEFAULT_FILEPATH):
    """Return all stored feedback entries.

    Args:
        filepath: Path to the JSON file used for storage.

    Returns:
        A list of dicts, each with keys 'rating', 'comment', and 'timestamp'.
    """
    return _load(filepath)


def get_average_rating(filepath=DEFAULT_FILEPATH):
    """Return the mean rating across all stored feedback.

    Args:
        filepath: Path to the JSON file used for storage.

    Returns:
        A float representing the average rating, or None if there is no feedback.
    """
    entries = _load(filepath)
    if not entries:
        return None
    return sum(e["rating"] for e in entries) / len(entries)


def _load(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(filepath, entries):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
