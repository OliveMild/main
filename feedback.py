#!/usr/bin/env python3
"""User feedback module for collecting and storing user feedback."""

import json
from datetime import datetime


FEEDBACK_FILE = "feedback.json"


def collect_feedback():
    """Prompt the user for feedback and return a feedback dictionary."""
    print("\n--- User Feedback ---")

    while True:
        try:
            rating = int(input("Please rate your experience (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Rating must be between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

    comment = input("Any additional comments? ").strip()

    return {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
    }


def save_feedback(feedback, filepath=FEEDBACK_FILE):
    """Save feedback to a JSON file."""
    existing = []
    try:
        with open(filepath, "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        pass

    existing.append(feedback)

    with open(filepath, "w") as f:
        json.dump(existing, f, indent=2)


def submit_feedback():
    """Collect feedback from the user and save it."""
    feedback = collect_feedback()
    save_feedback(feedback)
    print("\nThank you for your feedback!")
    return feedback


if __name__ == "__main__":
    submit_feedback()
