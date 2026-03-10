#!/usr/bin/env python3

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback.json"


def collect_feedback():
    """Prompt the user for a rating and optional comment; return a timestamped dict."""
    print("\n--- User Feedback ---")
    while True:
        try:
            rating = int(input("Please rate your experience (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Rating must be between 1 and 5.")
        except ValueError:
            print("Please enter a number between 1 and 5.")

    comment = input("Any additional comments? ").strip()
    return {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_feedback(feedback, filepath=None):
    """Append a feedback entry to the JSON file at *filepath*."""
    if filepath is None:
        filepath = FEEDBACK_FILE
    entries = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError):
        pass

    entries.append(feedback)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback():
    """Collect feedback from the user, save it, and confirm."""
    feedback = collect_feedback()
    save_feedback(feedback)
    print("\nThank you for your feedback!")
