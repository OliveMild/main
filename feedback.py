#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback entries."""

import json
import os

FEEDBACK_FILE = "feedback.json"


def _load_feedback():
    """Load feedback from the JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _save_feedback(feedback_list):
    """Save feedback to the JSON file."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_list, f, indent=2)


def submit_feedback(user: str, message: str, rating: int) -> dict:
    """Submit a new feedback entry.

    Args:
        user: The name of the user submitting feedback.
        message: The feedback message.
        rating: A rating between 1 and 5 (inclusive).

    Returns:
        The newly created feedback entry.

    Raises:
        ValueError: If rating is not between 1 and 5.
    """
    if not user or not user.strip():
        raise ValueError("User must not be empty")
    if not message or not message.strip():
        raise ValueError("Message must not be empty")
    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5")

    feedback_list = _load_feedback()
    next_id = max((entry["id"] for entry in feedback_list), default=0) + 1
    entry = {
        "id": next_id,
        "user": user,
        "message": message,
        "rating": rating,
    }
    feedback_list.append(entry)
    _save_feedback(feedback_list)
    return entry


def get_feedback() -> list:
    """Retrieve all feedback entries.

    Returns:
        A list of all feedback entries.
    """
    return _load_feedback()


def get_average_rating() -> float:
    """Calculate the average rating across all feedback entries.

    Returns:
        The average rating, or 0.0 if there are no entries.
    """
    feedback_list = _load_feedback()
    if not feedback_list:
        return 0.0
    return sum(entry["rating"] for entry in feedback_list) / len(feedback_list)
