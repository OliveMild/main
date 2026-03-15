#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback."""

import json
import os
from datetime import datetime, timezone


FEEDBACK_FILE = "feedback.json"


def _load_feedback(filepath=FEEDBACK_FILE):
    """Load existing feedback from file."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_feedback(entries, filepath=FEEDBACK_FILE):
    """Save feedback entries to file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback(rating, comment="", filepath=FEEDBACK_FILE):
    """Submit user feedback with a rating (1-5) and optional comment.

    Args:
        rating: Integer between 1 and 5.
        comment: Optional text comment.
        filepath: Path to the feedback storage file.

    Returns:
        The new feedback entry as a dict.

    Raises:
        ValueError: If rating is not between 1 and 5.
    """
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")

    entry = {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    entries = _load_feedback(filepath)
    entries.append(entry)
    _save_feedback(entries, filepath)
    return entry


def get_all_feedback(filepath=FEEDBACK_FILE):
    """Return all stored feedback entries.

    Args:
        filepath: Path to the feedback storage file.

    Returns:
        List of feedback entry dicts.
    """
    return _load_feedback(filepath)


def get_average_rating(filepath=FEEDBACK_FILE):
    """Calculate the average rating from all feedback.

    Args:
        filepath: Path to the feedback storage file.

    Returns:
        Average rating as a float, or None if no feedback exists.
    """
    entries = _load_feedback(filepath)
    if not entries:
        return None
    return sum(e["rating"] for e in entries) / len(entries)


if __name__ == "__main__":
    print("User Feedback Module")
    print("Submit feedback by calling submit_feedback(rating, comment).")
