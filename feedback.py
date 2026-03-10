#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback."""

from datetime import datetime


class Feedback:
    """Represents a single piece of user feedback."""

    def __init__(self, user: str, message: str, rating: int):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.user = user
        self.message = message
        self.rating = rating
        self.timestamp = datetime.now()

    def __str__(self):
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.user} (rating: {self.rating}/5): {self.message}"
        )


class FeedbackManager:
    """Manages a collection of user feedback entries."""

    def __init__(self):
        self._feedbacks: list[Feedback] = []

    def add_feedback(self, user: str, message: str, rating: int) -> Feedback:
        """Add a new feedback entry and return it."""
        feedback = Feedback(user, message, rating)
        self._feedbacks.append(feedback)
        return feedback

    def get_all_feedback(self) -> list[Feedback]:
        """Return all feedback entries."""
        return list(self._feedbacks)

    def get_average_rating(self) -> float:
        """Return the average rating across all feedback, or 0.0 if none."""
        if not self._feedbacks:
            return 0.0
        return sum(f.rating for f in self._feedbacks) / len(self._feedbacks)

    def display_feedback(self) -> None:
        """Print all feedback entries to stdout."""
        if not self._feedbacks:
            print("No feedback submitted yet.")
            return
        for feedback in self._feedbacks:
            print(feedback)
        print(f"Average rating: {self.get_average_rating():.1f}/5")


if __name__ == "__main__":
    manager = FeedbackManager()
    manager.add_feedback("Alice", "Great product!", 5)
    manager.add_feedback("Bob", "Could be improved.", 3)
    manager.display_feedback()
