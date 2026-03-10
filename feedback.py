_feedbacks = []


def submit_feedback(rating, comment=None):
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    if not (1 <= rating <= 5):
        raise ValueError("rating must be between 1 and 5")
    _feedbacks.append({"rating": rating, "comment": comment})


def get_average_rating():
    if not _feedbacks:
        return None
    return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)
