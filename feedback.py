#!/usr/bin/env python3
"""User feedback module for collecting and storing feedback."""

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback_data.json"


def load_feedback():
    """Load existing feedback from storage."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def save_feedback(feedback_list):
    """Save feedback list to storage."""
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)


def submit_feedback(message, rating=None):
    """Submit a new feedback entry.

    Args:
        message: The feedback message text.
        rating: Optional numeric rating (1-5).

    Returns:
        The newly created feedback entry dict.
    """
    if not message or not message.strip():
        raise ValueError("Feedback message cannot be empty.")
    if rating is not None and rating not in range(1, 6):
        raise ValueError("Rating must be between 1 and 5.")

    entry = {
        "message": message.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if rating is not None:
        entry["rating"] = rating

    feedback_list = load_feedback()
    feedback_list.append(entry)
    save_feedback(feedback_list)
    return entry


def get_all_feedback():
    """Return all submitted feedback entries."""
    return load_feedback()


def main():
    """Interactive CLI for the feedback feature."""
    print("=== User Feedback ===")
    print("1. Submit feedback")
    print("2. View all feedback")
    print("3. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        message = input("Enter your feedback: ").strip()
        rating_input = input("Enter a rating (1-5, or press Enter to skip): ").strip()
        try:
            rating = int(rating_input) if rating_input else None
        except ValueError:
            print("Error: Rating must be a number.")
            return
        try:
            entry = submit_feedback(message, rating)
            print("Thank you! Your feedback has been recorded.")
            print(f"  Message : {entry['message']}")
            if "rating" in entry:
                print(f"  Rating  : {entry['rating']}/5")
        except ValueError as e:
            print(f"Error: {e}")
    elif choice == "2":
        entries = get_all_feedback()
        if not entries:
            print("No feedback has been submitted yet.")
        else:
            print(f"\n{len(entries)} feedback entry/entries:\n")
            for i, entry in enumerate(entries, 1):
                print(f"  [{i}] {entry['timestamp']}")
                print(f"       Message : {entry['message']}")
                if "rating" in entry:
                    print(f"       Rating  : {entry['rating']}/5")
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
