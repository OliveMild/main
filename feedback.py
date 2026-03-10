#!/usr/bin/env python3
"""User feedback module for collecting, persisting, and summarizing ratings."""

import json
import datetime

DEFAULT_FILEPATH = "feedback.json"


def submit_feedback(rating, comment="", filepath=DEFAULT_FILEPATH):
    """Validate and persist a feedback entry.

    Args:
        rating: Integer rating between 1 and 5 (inclusive).
        comment: Optional string comment.
        filepath: Path to the JSON file used for storage.

    Raises:
        TypeError: If rating is not an int (booleans are rejected).
        ValueError: If rating is not between 1 and 5.
    """
    if isinstance(rating, bool) or not isinstance(rating, int):
        raise TypeError("rating must be an integer")
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")

    entry = {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    entries = get_all_feedback(filepath)
    entries.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    return entry


def get_all_feedback(filepath=DEFAULT_FILEPATH):
    """Return all stored feedback entries.

    Args:
        filepath: Path to the JSON file used for storage.

    Returns:
        List of feedback entry dicts.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def get_average_rating(filepath=DEFAULT_FILEPATH):
    """Return the average rating across all stored entries.

    Args:
        filepath: Path to the JSON file used for storage.

    Returns:
        Mean rating as a float, or None if there are no entries.
    """
    entries = get_all_feedback(filepath)
    if not entries:
        return None
    return sum(e["rating"] for e in entries) / len(entries)
