#!/usr/bin/env python3

from datetime import datetime, timezone


class FeedbackManager:
    def __init__(self):
        self._entries = []

    def submit(self, message, rating):
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._entries.append({"message": message, "rating": rating, "timestamp": timestamp})

    def display(self):
        lines = []
        for i, entry in enumerate(self._entries, start=1):
            lines.append(f"{i}. [{entry['rating']}/5] {entry['message']}  ({entry['timestamp']})")
        if self._entries:
            avg = sum(e["rating"] for e in self._entries) / len(self._entries)
            lines.append(f"Average rating: {avg:g}/5")
        return "\n".join(lines)


if __name__ == "__main__":
    manager = FeedbackManager()
    manager.submit("Great app!", 5)
    manager.submit("Needs work", 2)
    print(manager.display())
