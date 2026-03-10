#!/usr/bin/env python3

from feedback import FeedbackError, FeedbackManager


def collect_feedback(manager: FeedbackManager) -> None:
    """Interactively collect feedback from the user."""
    print("\n--- User Feedback ---")
    message = input("Enter your feedback: ")
    try:
        rating = int(input("Enter a rating (1-5): "))
    except ValueError:
        print("Invalid rating. Please enter a whole number between 1 and 5.")
        return
    try:
        manager.submit(message, rating)
        print("Thank you for your feedback!")
    except FeedbackError as exc:
        print(f"Could not submit feedback: {exc}")


if __name__ == "__main__":
    print("Hello World")
    manager = FeedbackManager()
    collect_feedback(manager)
    print("\n--- All Feedback ---")
    print(manager.display())
