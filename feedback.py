#!/usr/bin/env python3
"""User feedback module providing FeedbackManager and FeedbackError."""

from datetime import datetime, timezone


class FeedbackError(Exception):
    """Raised when feedback submission contains invalid data."""


class FeedbackManager:
    """Manages user feedback entries with ratings."""

    def __init__(self):
        self._entries = []

    def submit(self, message: str, rating: int) -> None:
        """Submit a feedback entry.

        Args:
            message: Non-empty feedback text.
            rating: Integer rating between 1 and 5 inclusive.

        Raises:
            FeedbackError: If message is empty or rating is invalid.
        """
        if not isinstance(message, str) or not message.strip():
            raise FeedbackError("Feedback message must not be empty.")
        if not isinstance(rating, int) or isinstance(rating, bool):
            raise FeedbackError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise FeedbackError("Rating must be between 1 and 5.")
        self._entries.append({
            "message": message,
            "rating": rating,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        })

    def get_all(self) -> list:
        """Return a copy of all feedback entries."""
        return list(self._entries)

    def average_rating(self) -> float:
        """Return the average rating across all entries.

        Returns:
            The average rating, or 0.0 if there are no entries.
        """
        if not self._entries:
            return 0.0
        return sum(e["rating"] for e in self._entries) / len(self._entries)

    def display(self) -> str:
        """Return a formatted string of all feedback entries."""
        if not self._entries:
            return "No feedback submitted yet."
        lines = []
        for i, entry in enumerate(self._entries, start=1):
            lines.append(
                f"{i}. [{entry['rating']}/5] {entry['message']}  ({entry['timestamp']})"
            )
        lines.append(f"Average rating: {self.average_rating()}/5")
        return "\n".join(lines)
