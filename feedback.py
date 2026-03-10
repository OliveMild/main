"""User feedback module for collecting and analyzing feedback."""

_feedbacks = []


def submit_feedback(rating, message=None):
    """Submit user feedback with a rating and optional message.

    Args:
        rating: Numeric rating between 1 and 5 (inclusive).
        message: Optional feedback message string.

    Raises:
        ValueError: If rating is not a number or not in the range 1-5.
    """
    if isinstance(rating, bool) or not isinstance(rating, (int, float)):
        raise ValueError(f"Rating must be a number, got {type(rating).__name__!r}")
    if not (1 <= rating <= 5):
        raise ValueError(f"Rating must be between 1 and 5, got {rating!r}")
    _feedbacks.append({"rating": rating, "message": message})


def get_average_rating():
    """Return the average rating across all submitted feedback.

    Returns:
        The average rating as a float, or 0.0 if no feedback has been submitted.
    """
    if not _feedbacks:
        return 0.0
    return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)
