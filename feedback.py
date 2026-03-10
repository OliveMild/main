#!/usr/bin/env python3
"""User feedback module for collecting and viewing feedback."""

import json
import os
import sys
from datetime import datetime, timezone

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback.json")


def _load_feedback():
    """Load existing feedback from the JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return []
    return json.loads(content)


def _save_feedback(entries):
    """Save feedback entries to the JSON file."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def submit_feedback(rating, comment):
    """Submit a new feedback entry.

    Args:
        rating: An integer from 1 to 5.
        comment: A non-empty string with the feedback comment.

    Returns:
        The saved feedback entry as a dict.

    Raises:
        ValueError: If rating or comment are invalid.
    """
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")
    if not isinstance(comment, str) or not comment.strip():
        raise ValueError("Comment must be a non-empty string.")

    entry = {
        "rating": rating,
        "comment": comment.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    entries = _load_feedback()
    entries.append(entry)
    _save_feedback(entries)
    return entry


def view_feedback():
    """Return all feedback entries.

    Returns:
        A list of feedback entry dicts.
    """
    return _load_feedback()


def _print_feedback(entries):
    """Print feedback entries to stdout."""
    if not entries:
        print("No feedback submitted yet.")
        return
    for i, entry in enumerate(entries, start=1):
        print(f"[{i}] Rating: {entry['rating']}/5 | {entry['timestamp']}")
        print(f"    {entry['comment']}")


def main():
    """CLI entry point for the feedback feature."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  feedback.py submit <rating 1-5> <comment>")
        print("  feedback.py view")
        sys.exit(1)

    command = sys.argv[1]

    if command == "submit":
        if len(sys.argv) < 4:
            print("Usage: feedback.py submit <rating 1-5> <comment>")
            sys.exit(1)
        try:
            rating = int(sys.argv[2])
        except ValueError:
            print("Error: Rating must be an integer between 1 and 5.")
            sys.exit(1)
        comment = " ".join(sys.argv[3:])
        try:
            entry = submit_feedback(rating, comment)
            print(f"Feedback submitted: rating={entry['rating']}, comment=\"{entry['comment']}\"")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "view":
        entries = view_feedback()
        _print_feedback(entries)

    else:
        print(f"Unknown command: {command}")
        print("Valid commands: submit, view")
        sys.exit(1)


if __name__ == "__main__":
    main()
