#!/usr/bin/env python3
"""User feed module for posting, retrieving, and displaying feed items."""

import datetime
import json

DEFAULT_FILEPATH = "feed.json"


def post_to_feed(user, content, filepath=DEFAULT_FILEPATH):
    """Add a new post to the user feed.

    Args:
        user: Non-empty string identifying the author.
        content: Non-empty string with the post content.
        filepath: Path to the JSON file used for storage.

    Returns:
        The newly created feed entry dict.

    Raises:
        TypeError: If user or content is not a string.
        ValueError: If user or content is empty.
    """
    if not isinstance(user, str):
        raise TypeError("user must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not user.strip():
        raise ValueError("user must not be empty")
    if not content.strip():
        raise ValueError("content must not be empty")

    entry = {
        "user": user.strip(),
        "content": content.strip(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    entries = get_feed(filepath)
    entries.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    return entry


def get_feed(filepath=DEFAULT_FILEPATH):
    """Return all stored feed entries, newest first.

    Args:
        filepath: Path to the JSON file used for storage.

    Returns:
        List of feed entry dicts sorted by timestamp descending.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    return sorted(entries, key=lambda e: e.get("timestamp", ""), reverse=True)


def display_feed(filepath=DEFAULT_FILEPATH):
    """Print all feed entries to stdout in a readable format.

    Args:
        filepath: Path to the JSON file used for storage.
    """
    entries = get_feed(filepath)
    if not entries:
        print("No posts yet.")
        return
    print("\n--- User Feed ---")
    for entry in entries:
        print(f"[{entry['timestamp']}] {entry['user']}: {entry['content']}")
    print("-----------------")
