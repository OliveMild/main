#!/usr/bin/env python3
from datetime import datetime, timezone


class FeedbackManager:
    def __init__(self):
        self._entries = []

    def submit(self, text: str, rating: int) -> None:
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self._entries.append({
            "text": text,
            "rating": rating,
            "timestamp": datetime.now(timezone.utc),
        })

    def display(self) -> str:
        if not self._entries:
            return "No feedback submitted yet."
        lines = []
        total = 0
        for i, entry in enumerate(self._entries, start=1):
            ts = entry["timestamp"].isoformat(timespec="seconds")
            lines.append(f"{i}. [{entry['rating']}/5] {entry['text']}  ({ts})")
            total += entry["rating"]
        avg_rating = total / len(self._entries)
        lines.append(f"Average rating: {avg_rating:g}/5")
        return "\n".join(lines)


if __name__ == "__main__":
    manager = FeedbackManager()
    manager.submit("Great app!", 5)
    manager.submit("Needs work", 2)
    print(manager.display())
