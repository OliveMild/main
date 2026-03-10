#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback."""

import json
import os
from datetime import datetime, timezone

_FEEDBACK_FILE = "feedback.json"


def _load_feedback(filepath=_FEEDBACK_FILE):
    """Load feedback entries from a JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_feedback(entries, filepath=_FEEDBACK_FILE):
    """Save feedback entries to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback(rating, comment="", filepath=_FEEDBACK_FILE):
    """Submit a new feedback entry.

    Args:
        rating: An integer from 1 to 5.
        comment: Optional text comment.
        filepath: Path to the feedback storage file.

    Returns:
        The newly created feedback entry as a dict.

    Raises:
        ValueError: If rating is not between 1 and 5.
    """
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")

    entry = {
        "rating": rating,
        "comment": comment.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    entries = _load_feedback(filepath)
    entries.append(entry)
    _save_feedback(entries, filepath)

    return entry


def get_feedback(filepath=_FEEDBACK_FILE):
    """Return all feedback entries.

    Args:
        filepath: Path to the feedback storage file.

    Returns:
        A list of feedback entry dicts.
    """
    return _load_feedback(filepath)


def get_average_rating(filepath=_FEEDBACK_FILE):
    """Return the average rating across all feedback entries.

    Args:
        filepath: Path to the feedback storage file.

    Returns:
        The average rating as a float, or None if there is no feedback.
    """
    entries = _load_feedback(filepath)
    if not entries:
        return None
    return sum(e["rating"] for e in entries) / len(entries)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python feedback.py <rating> [comment]")
        print("  rating: integer 1-5")
        sys.exit(1)

    try:
        user_rating = int(sys.argv[1])
    except ValueError:
        print("Error: rating must be an integer.")
        sys.exit(1)

    user_comment = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    new_entry = submit_feedback(user_rating, user_comment)
    print(f"Feedback submitted: rating={new_entry['rating']}, comment='{new_entry['comment']}'")

    avg = get_average_rating()
    if avg is not None:
        print(f"Average rating: {avg:.2f}")
    else:
        print("Average rating: No feedback yet")
