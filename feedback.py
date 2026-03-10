#!/usr/bin/env python3
"""User feedback collection module."""

import json
import os

FEEDBACK_FILE = "feedback.json"


def collect_feedback():
    """Prompt the user for a rating and optional comment.

    Returns a dict with keys 'rating' (int, 1-5) and 'comment' (str).
    Re-prompts until a valid rating in the range 1-5 is entered.
    """
    print("\n--- User Feedback ---")
    while True:
        raw = input("Please rate your experience (1-5): ").strip()
        try:
            rating = int(raw)
        except ValueError:
            print("Please enter a number between 1 and 5.")
            continue
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            continue
        break

    comment = input("Any additional comments? (press Enter to skip): ").strip()
    return {"rating": rating, "comment": comment}


def save_feedback(entry, filepath=FEEDBACK_FILE):
    """Append a feedback entry to the JSON file."""
    entries = load_feedback(filepath)
    entries.append(entry)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def load_feedback(filepath=FEEDBACK_FILE):
    """Load and return all feedback entries from the JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def run_feedback():
    """Collect feedback from the user and persist it."""
    entry = collect_feedback()
    save_feedback(entry)
    print("Thank you for your feedback!")
