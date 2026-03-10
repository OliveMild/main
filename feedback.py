"""User feedback module for collecting ratings and comments."""

_feedbacks = []


def submit_feedback(rating, comment=None):
    """Submit a user feedback entry.

    Args:
        rating: A numeric rating value.
        comment: An optional comment string.

    Raises:
        TypeError: If rating is not a numeric type.
    """
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    _feedbacks.append({"rating": rating, "comment": comment})


def get_average_rating():
    """Return the average rating of all submitted feedbacks.

    Returns:
        The average rating as a float, or None if no feedbacks have been submitted.
    """
    if not _feedbacks:
        return None
    return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)
