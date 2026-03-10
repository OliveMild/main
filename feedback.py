#!/usr/bin/env python3
"""User feedback module: collect, store, and display feedback entries."""

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback.json"


def load_feedback():
    """Load feedback entries from the JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_feedback(entries):
    """Save feedback entries to the JSON file."""
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Warning: could not save feedback: {e}")


def collect_feedback():
    """Prompt the user for feedback and append it to the feedback file."""
    print("\n--- User Feedback ---")
    name = input("Your name (or leave blank for anonymous): ").strip()
    if not name:
        name = "Anonymous"
    message = input("Your feedback: ").strip()
    if not message:
        print("No feedback entered.")
        return

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "message": message,
    }

    entries = load_feedback()
    entries.append(entry)
    save_feedback(entries)
    print("Thank you for your feedback!")


def display_feedback():
    """Print all stored feedback entries."""
    entries = load_feedback()
    print("\n--- Feedback Received ---")
    if not entries:
        print("No feedback yet.")
        return
    for entry in entries:
        timestamp = entry.get("timestamp", "unknown time")
        name = entry.get("name", "Anonymous")
        message = entry.get("message", "")
        print(f"[{timestamp}] {name}: {message}")
