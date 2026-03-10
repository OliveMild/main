#!/usr/bin/env python3
"""User feedback module for collecting and managing feedback."""

from datetime import datetime, timezone


class FeedbackError(ValueError):
    """Raised when feedback input is invalid."""


class FeedbackManager:
    """Manages user feedback: submission, storage, and retrieval."""

    def __init__(self):
        self._feedback_list = []

    def submit(self, message: str, rating: int) -> dict:
        """Submit new feedback.

        Args:
            message: Feedback message text (must be non-empty).
            rating: Rating between 1 and 5 inclusive.

        Returns:
            The stored feedback entry as a dict.

        Raises:
            FeedbackError: If message is empty or rating is out of range.
        """
        if not message or not message.strip():
            raise FeedbackError("Feedback message must not be empty.")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise FeedbackError("Rating must be an integer between 1 and 5.")

        entry = {
            "message": message.strip(),
            "rating": rating,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._feedback_list.append(entry)
        return entry

    def get_all(self) -> list:
        """Return all submitted feedback entries."""
        return list(self._feedback_list)

    def average_rating(self) -> float:
        """Return the average rating, or 0.0 if no feedback has been submitted."""
        if not self._feedback_list:
            return 0.0
        return sum(e["rating"] for e in self._feedback_list) / len(self._feedback_list)

    def display(self) -> str:
        """Return a formatted string of all feedback for display."""
        if not self._feedback_list:
            return "No feedback submitted yet."
        lines = []
        for i, entry in enumerate(self._feedback_list, start=1):
            lines.append(
                f"{i}. [{entry['rating']}/5] {entry['message']}  ({entry['timestamp']})"
            )
        lines.append(f"\nAverage rating: {self.average_rating():.1f}/5")
        return "\n".join(lines)
