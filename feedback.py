#!/usr/bin/env python3
"""User feedback module for collecting and displaying feedback."""

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback_data.json"


def _load_feedback():
    """Load feedback entries from the storage file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_feedback(entries):
    """Save feedback entries to the storage file."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback(message, rating=None):
    """Submit a new feedback entry.

    Args:
        message: The feedback text (non-empty string).
        rating: Optional integer rating between 1 and 5.

    Returns:
        The newly created feedback entry as a dict.

    Raises:
        ValueError: If message is empty or rating is out of range.
    """
    if not message or not message.strip():
        raise ValueError("Feedback message cannot be empty.")
    if rating is not None and rating not in range(1, 6):
        raise ValueError("Rating must be an integer between 1 and 5.")

    entries = _load_feedback()
    next_id = max((e["id"] for e in entries), default=0) + 1
    entry = {
        "id": next_id,
        "message": message.strip(),
        "rating": rating,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    entries.append(entry)
    _save_feedback(entries)
    return entry


def get_feedback():
    """Return all feedback entries.

    Returns:
        A list of feedback entry dicts ordered by submission time.
    """
    return _load_feedback()


def display_feedback():
    """Print all feedback entries to stdout in a human-readable format."""
    entries = get_feedback()
    if not entries:
        print("No feedback submitted yet.")
        return
    print(f"{'='*40}")
    print(f"Total feedback entries: {len(entries)}")
    print(f"{'='*40}")
    for entry in entries:
        rating_str = f"  Rating: {entry['rating']}/5" if entry["rating"] is not None else ""
        print(f"[#{entry['id']}] {entry['timestamp']}")
        print(f"  {entry['message']}{rating_str}")
    print(f"{'='*40}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args or args[0] == "view":
        display_feedback()
    elif args[0] == "submit":
        if len(args) < 2:
            print("Usage: feedback.py submit <message> [rating]")
            sys.exit(1)
        msg = args[1]
        rating = None
        if len(args) > 2:
            try:
                rating = int(args[2])
            except ValueError:
                print(f"Error: rating must be an integer between 1 and 5, got '{args[2]}'")
                sys.exit(1)
        entry = submit_feedback(msg, rating)
        print(f"Feedback submitted (id={entry['id']}): {entry['message']}")
    else:
        print("Usage: feedback.py [view | submit <message> [rating]]")
        sys.exit(1)
