_feedbacks = []


def submit_feedback(rating, comment=None):
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    _feedbacks.append({"rating": rating, "comment": comment})


def get_average_rating():
    if not _feedbacks:
        return None
    return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)


def clear_feedbacks():
    _feedbacks.clear()
