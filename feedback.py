#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback entries."""

import json
import os

FEEDBACK_FILE = "feedback.json"


def _load_feedback() -> list:
    """Load feedback entries from the JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_feedback(entries: list) -> None:
    """Save feedback entries to the JSON file."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback(user: str, message: str, rating: int) -> dict:
    """Submit a new feedback entry.

    Args:
        user: Name of the user submitting feedback.
        message: Feedback message text.
        rating: Numeric rating between 1 and 5 (inclusive).

    Returns:
        The newly created feedback entry as a dict.

    Raises:
        ValueError: If rating is not between 1 and 5.
    """
    if not 1 <= rating <= 5:
        raise ValueError(f"Rating must be between 1 and 5, got {rating}")

    entries = _load_feedback()
    entry = {
        "id": max((e["id"] for e in entries), default=0) + 1,
        "user": user,
        "message": message,
        "rating": rating,
    }
    entries.append(entry)
    _save_feedback(entries)
    return entry


def get_feedback() -> list:
    """Return all feedback entries.

    Returns:
        A list of feedback entry dicts.
    """
    return _load_feedback()


def get_average_rating() -> float:
    """Calculate the average rating across all feedback entries.

    Returns:
        The average rating, or 0.0 if there are no entries.
    """
    entries = _load_feedback()
    if not entries:
        return 0.0
    return sum(e["rating"] for e in entries) / len(entries)
