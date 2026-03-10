#!/usr/bin/env python3

_feedback_entries = []


def submit_feedback(rating, comment=None):
    """Submit user feedback with a rating and optional comment.

    Args:
        rating: A numeric rating value between 1 and 5.
        comment: An optional text comment (default: None).

    Raises:
        TypeError: If rating is not a number.
        ValueError: If rating is not between 1 and 5.
    """
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    if not 1 <= rating <= 5:
        raise ValueError("rating must be between 1 and 5")
    _feedback_entries.append({"rating": rating, "comment": comment})


def get_average_rating():
    """Return the average rating of all submitted feedback.

    Returns:
        The average rating as a float, or 0.0 if no feedback has been submitted.
    """
    if not _feedback_entries:
        return 0.0
    return sum(entry["rating"] for entry in _feedback_entries) / len(_feedback_entries)
