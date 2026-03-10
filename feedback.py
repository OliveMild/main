#!/usr/bin/env python3
"""User feedback module for collecting and displaying feedback."""

from datetime import datetime, timezone


class FeedbackCollector:
    """Collects and manages user feedback entries."""

    def __init__(self):
        self._feedback = []

    def submit(self, rating: int, comment: str = "") -> dict:
        """Submit a feedback entry with a rating (1-5) and optional comment.

        Args:
            rating: An integer rating from 1 to 5.
            comment: An optional text comment.

        Returns:
            The submitted feedback entry.

        Raises:
            ValueError: If rating is not between 1 and 5.
        """
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        entry = {
            "rating": rating,
            "comment": comment.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._feedback.append(entry)
        return entry

    def get_all(self) -> list:
        """Return all submitted feedback entries."""
        return list(self._feedback)

    def average_rating(self) -> float:
        """Return the average rating, or 0.0 if no feedback has been submitted."""
        if not self._feedback:
            return 0.0
        return sum(e["rating"] for e in self._feedback) / len(self._feedback)

    def display(self) -> None:
        """Print all feedback entries to stdout."""
        if not self._feedback:
            print("No feedback submitted yet.")
            return
        print(f"=== User Feedback ({len(self._feedback)} entries) ===")
        for i, entry in enumerate(self._feedback, start=1):
            stars = "*" * entry["rating"]
            comment = f" - {entry['comment']}" if entry["comment"] else ""
            print(f"  {i}. [{stars}] {entry['timestamp']}{comment}")
        print(f"Average rating: {self.average_rating():.1f} / 5.0")
