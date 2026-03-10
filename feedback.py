import json
import os

FEEDBACK_FILE = "feedback_data.json"


def load_feedback():
    """Load feedback entries from the JSON store."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def submit_feedback(rating, comment=""):
    """Submit a feedback entry with a rating (1–5) and optional comment."""
    if not isinstance(rating, int) or isinstance(rating, bool) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")
    entries = load_feedback()
    entries.append({"rating": rating, "comment": comment})
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def get_average_rating():
    """Return the average rating across all feedback entries, or 0.0 if none."""
    entries = load_feedback()
    if not entries:
        return 0.0
    return sum(e["rating"] for e in entries) / len(entries)
