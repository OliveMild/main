#!/usr/bin/env python3
"""User feedback module for collecting and storing feedback."""

import json
import os
from datetime import datetime, timezone


FEEDBACK_FILE = "feedback.json"


def collect_feedback():
    """Prompt the user for a rating and optional comment."""
    print("\n--- User Feedback ---")
    rating = None
    while rating is None:
        try:
            value = int(input("Please rate your experience (1-5): "))
            if 1 <= value <= 5:
                rating = value
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    comment = input("Any additional comments? (press Enter to skip): ").strip()
    return {"rating": rating, "comment": comment, "timestamp": datetime.now(timezone.utc).isoformat()}


def save_feedback(entry, filepath=FEEDBACK_FILE):
    """Append a feedback entry to the JSON feedback file."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_feedback(filepath=FEEDBACK_FILE):
    """Load all feedback entries from the JSON feedback file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def run_feedback():
    """Collect feedback from the user and save it."""
    entry = collect_feedback()
    save_feedback(entry)
    print("Thank you for your feedback!")
