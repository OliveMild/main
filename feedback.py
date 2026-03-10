import threading

_lock = threading.Lock()
_feedbacks = []


def submit_feedback(rating, comment=None):
    if not isinstance(rating, (int, float)):
        raise TypeError("rating must be a numeric value")
    with _lock:
        _feedbacks.append({"rating": rating, "comment": comment})


def get_average_rating():
    with _lock:
        if not _feedbacks:
            return None
        return sum(f["rating"] for f in _feedbacks) / len(_feedbacks)
