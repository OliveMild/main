#!/usr/bin/env python3

import json
import os
from datetime import datetime

FEEDBACK_FILE = "feedback.json"


def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return []


def save_feedback(feedback_list):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)


def submit_feedback():
    print("\n--- Submit Feedback ---")
    while True:
        try:
            rating = int(input("Rate your experience (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    comment = input("Leave a comment (optional): ").strip()
    entry = {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
    }
    feedback_list = load_feedback()
    feedback_list.append(entry)
    save_feedback(feedback_list)
    print("Thank you for your feedback!")


def view_feedback():
    feedback_list = load_feedback()
    if not feedback_list:
        print("\nNo feedback submitted yet.")
        return
    print(f"\n--- Feedback ({len(feedback_list)} entries) ---")
    for i, entry in enumerate(feedback_list, 1):
        print(f"{i}. Rating: {entry['rating']}/5 | {entry['timestamp']}")
        if entry.get("comment"):
            print(f"   Comment: {entry['comment']}")
    avg = sum(e["rating"] for e in feedback_list) / len(feedback_list)
    print(f"\nAverage rating: {avg:.1f}/5")


def main():
    print("Hello World")
    print("\nWhat would you like to do?")
    print("1. Submit feedback")
    print("2. View feedback")
    print("3. Exit")
    choice = input("Enter choice (1-3): ").strip()
    if choice == "1":
        submit_feedback()
    elif choice == "2":
        view_feedback()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
