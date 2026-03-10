#!/usr/bin/env python3

from feedback import FeedbackManager, FeedbackError


def collect_feedback(manager: FeedbackManager) -> None:
    """Prompt the user to submit a feedback entry."""
    message = input("Enter your feedback message: ")
    rating_input = input("Enter your rating (1-5): ")
    try:
        rating = int(rating_input)
    except ValueError:
        raise FeedbackError("Rating must be an integer.")
    manager.submit(message, rating)


if __name__ == "__main__":
    print("Hello World")

    feedback_manager = FeedbackManager()
    print("\n--- Feedback ---")
    try:
        collect_feedback(feedback_manager)
    except FeedbackError as exc:
        print(f"Invalid feedback: {exc}")

    print("\n--- All Feedback ---")
    print(feedback_manager.display())
