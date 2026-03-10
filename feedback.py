"""User feedback module for collecting and querying feedback ratings."""

_feedback_store = []


def submit_feedback(rating, comment=None):
    """Submit a user feedback entry with a numeric rating and optional comment.

    Args:
        rating: A numeric rating value.
        comment: An optional string comment.

    Raises:
        TypeError: If rating is not numeric.
    """
    if isinstance(rating, bool) or not isinstance(rating, (int, float)):
        raise TypeError(f"Rating must be numeric, got {type(rating).__name__}")
    _feedback_store.append({"rating": rating, "comment": comment})


def get_average_rating():
    """Return the average of all submitted ratings.

    Returns:
        The mean rating as a float, or 0.0 if no feedback has been submitted.
    """
    if not _feedback_store:
        return 0.0
    return sum(entry["rating"] for entry in _feedback_store) / len(_feedback_store)
