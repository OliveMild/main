#!/usr/bin/env python3

from datetime import datetime, timezone


class FeedbackManager:
    def __init__(self):
        self._feedbacks = []

    def submit(self, text, rating):
        if not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
            raise ValueError("Rating must be a number between 1 and 5.")
        self._feedbacks.append({
            "text": text,
            "rating": rating,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def display(self):
        if not self._feedbacks:
            return "No feedback submitted yet."

        lines = []
        for i, fb in enumerate(self._feedbacks, start=1):
            lines.append(f"{i}. [{fb['rating']}/5] {fb['text']}  ({fb['timestamp']})")

        average = round(sum(fb["rating"] for fb in self._feedbacks) / len(self._feedbacks), 2)
        lines.append(f"Average rating: {average}/5")

        return "\n".join(lines)
