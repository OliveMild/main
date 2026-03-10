#!/usr/bin/env python3
"""User feedback module for collecting and storing user feedback."""

import json
import os
from datetime import datetime, timezone


FEEDBACK_FILE = "feedback.json"


def load_feedback():
    """Load existing feedback from the feedback file."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            content = f.read().strip()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return []
    return []


def save_feedback(feedback_list):
    """Save the feedback list to the feedback file."""
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)


def submit_feedback(user_name, message):
    """Submit user feedback.

    Args:
        user_name: The name of the user submitting feedback.
        message: The feedback message.

    Returns:
        The submitted feedback entry as a dict.

    Raises:
        ValueError: If user_name or message is empty.
    """
    if not user_name or not user_name.strip():
        raise ValueError("User name cannot be empty.")
    if not message or not message.strip():
        raise ValueError("Feedback message cannot be empty.")

    entry = {
        "user": user_name.strip(),
        "message": message.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    feedback_list = load_feedback()
    feedback_list.append(entry)
    save_feedback(feedback_list)

    return entry


def get_all_feedback():
    """Return all stored feedback entries."""
    return load_feedback()


def collect_feedback_from_user():
    """Interactively collect feedback from the user via stdin."""
    print("\n--- User Feedback ---")
    user_name = input("Your name: ").strip()
    message = input("Your feedback: ").strip()

    try:
        entry = submit_feedback(user_name, message)
        print(f"\nThank you, {entry['user']}! Your feedback has been recorded.")
    except ValueError as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    collect_feedback_from_user()
