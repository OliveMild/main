#!/usr/bin/env python3
"""User feedback module for collecting and storing feedback."""

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback_data.json"


def submit_feedback(rating: int, comment: str = "") -> dict:
    """Submit user feedback with a rating (1-5) and optional comment.

    Leading and trailing whitespace is stripped from the comment.
    """
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        raise ValueError("Rating must be an integer between 1 and 5.")

    entry = {
        "rating": rating,
        "comment": comment.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    feedback_list = load_feedback()
    feedback_list.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)

    return entry


def load_feedback() -> list:
    """Load all stored feedback entries. Returns an empty list if the file is missing or unreadable."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def get_average_rating() -> float:
    """Return the average rating from all feedback, or 0.0 if none."""
    feedback_list = load_feedback()
    if not feedback_list:
        return 0.0
    return sum(entry["rating"] for entry in feedback_list) / len(feedback_list)
