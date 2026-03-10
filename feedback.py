_feedbacks = []


def reset_feedback():
    """Clear all submitted feedback (useful for testing)."""
    _feedbacks.clear()


def submit_feedback(rating, comment=None):
    """Submit feedback with a numeric rating (1–5) and an optional comment."""
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    if not (1 <= rating <= 5):
        raise ValueError("rating must be between 1 and 5")
    _feedbacks.append({"rating": rating, "comment": comment})


def get_average_rating():
    """Return the average rating of all submitted feedback, or None if there is none."""
    if not _feedbacks:
        return None
    return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)
