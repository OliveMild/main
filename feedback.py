#!/usr/bin/env python3
"""User feedback module for collecting and displaying user feedback."""

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback.json"


def load_feedback():
    """Load existing feedback from the JSON file."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return []


def save_feedback(feedback_list):
    """Save feedback list to the JSON file."""
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)


def submit_feedback(name, rating, comment):
    """Submit new user feedback.

    Args:
        name: The name of the user submitting feedback.
        rating: A rating from 1 to 5.
        comment: A text comment from the user.

    Returns:
        The submitted feedback entry as a dict.

    Raises:
        ValueError: If rating is not between 1 and 5.
    """
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")

    entry = {
        "name": name,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    feedback_list = load_feedback()
    feedback_list.append(entry)
    save_feedback(feedback_list)
    return entry


def list_feedback():
    """Return all submitted feedback entries."""
    return load_feedback()


def get_average_rating():
    """Calculate and return the average rating across all feedback.

    Returns:
        The average rating as a float, or None if there is no feedback.
    """
    feedback_list = load_feedback()
    if not feedback_list:
        return None
    return sum(entry["rating"] for entry in feedback_list) / len(feedback_list)


def main():
    """Interactive CLI for the user feedback feature."""
    print("=== User Feedback System ===")
    print("1. Submit feedback")
    print("2. View all feedback")
    print("3. View average rating")
    print("4. Exit")

    while True:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            name = input("Your name: ").strip()
            try:
                rating = int(input("Rating (1-5): ").strip())
            except ValueError:
                print("Invalid rating. Please enter a number between 1 and 5.")
                continue
            comment = input("Comment: ").strip()
            try:
                entry = submit_feedback(name, rating, comment)
                print(f"Thank you, {entry['name']}! Your feedback has been recorded.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            entries = list_feedback()
            if not entries:
                print("No feedback submitted yet.")
            else:
                print(f"\n--- {len(entries)} feedback entry(s) ---")
                for entry in entries:
                    print(
                        f"[{entry['timestamp']}] {entry['name']} "
                        f"- Rating: {entry['rating']}/5 - {entry['comment']}"
                    )

        elif choice == "3":
            avg = get_average_rating()
            if avg is None:
                print("No feedback submitted yet.")
            else:
                print(f"Average rating: {avg:.2f}/5")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
