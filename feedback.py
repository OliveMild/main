#!/usr/bin/env python3

import json
import os
from datetime import datetime, timezone

FEEDBACK_FILE = "feedback.json"


def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: feedback file is corrupted. Starting with empty feedback.")
    return []


def save_feedback(feedback_list):
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedback_list, f, indent=2)
    except OSError as e:
        print(f"Error: could not save feedback: {e}")


def collect_feedback():
    print("\n--- User Feedback ---")
    name = input("Your name (or leave blank for anonymous): ").strip()
    if not name:
        name = "Anonymous"
    message = input("Your feedback: ").strip()
    if not message:
        print("No feedback provided.")
        return None

    entry = {
        "name": name,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    feedback_list = load_feedback()
    feedback_list.append(entry)
    save_feedback(feedback_list)

    print("Thank you for your feedback!")
    return entry


def display_feedback():
    feedback_list = load_feedback()
    if not feedback_list:
        print("No feedback yet.")
        return

    print("\n--- Feedback Received ---")
    for entry in feedback_list:
        timestamp = entry.get("timestamp", "unknown time")
        name = entry.get("name", "Unknown")
        message = entry.get("message", "")
        print(f"[{timestamp}] {name}: {message}")
