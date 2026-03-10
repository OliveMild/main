#!/usr/bin/env python3
"""User feedback module for submitting and viewing feedback entries."""

import json
import os
import sys

FEEDBACK_FILE = "feedback.json"


def submit_feedback(rating, comment):
    """Submit a feedback entry with a rating and comment.

    Args:
        rating: An integer between 1 and 5 (booleans are not accepted).
        comment: A non-empty string describing the feedback.

    Returns:
        The feedback entry dict that was stored.

    Raises:
        TypeError: If rating is not an int (or is a bool) or comment is not a str.
        ValueError: If rating is not in range 1–5 or comment is empty.
    """
    if isinstance(rating, bool) or not isinstance(rating, int):
        raise TypeError("rating must be an integer")
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")
    if not isinstance(comment, str):
        raise TypeError("comment must be a string")
    if not comment.strip():
        raise ValueError("comment must not be empty")

    entry = {"rating": rating, "comment": comment}

    entries = _load_entries()
    entries.append(entry)
    _save_entries(entries)

    return entry


def view_feedback():
    """Return all stored feedback entries.

    Returns:
        A list of feedback entry dicts.
    """
    return _load_entries()


def _load_entries():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_entries(entries):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def _main(args):
    if not args:
        print("Usage: feedback.py submit <rating> <comment>")
        print("       feedback.py view")
        sys.exit(1)

    command = args[0]

    if command == "submit":
        if len(args) < 3:
            print("Usage: feedback.py submit <rating> <comment>")
            sys.exit(1)
        try:
            rating = int(args[1])
        except ValueError:
            print("Error: rating must be an integer")
            sys.exit(1)
        comment = " ".join(args[2:])
        try:
            entry = submit_feedback(rating, comment)
            print(f"Feedback submitted: rating={entry['rating']}, comment={entry['comment']!r}")
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "view":
        entries = view_feedback()
        if not entries:
            print("No feedback entries found.")
        else:
            for i, entry in enumerate(entries, 1):
                print(f"{i}. rating={entry['rating']}, comment={entry['comment']!r}")

    else:
        print(f"Unknown command: {command!r}")
        print("Usage: feedback.py submit <rating> <comment>")
        print("       feedback.py view")
        sys.exit(1)


if __name__ == "__main__":
    _main(sys.argv[1:])
