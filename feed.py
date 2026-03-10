#!/usr/bin/env python3
"""User feed module for managing and displaying user activity feed items."""

import json
import os
from datetime import datetime, timezone

FEED_FILE = "feed_data.json"


def _load_feed():
    """Load feed entries from the storage file."""
    if not os.path.exists(FEED_FILE):
        return []
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_feed(entries):
    """Save feed entries to the storage file."""
    with open(FEED_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def add_feed_item(user, content, item_type="post"):
    """Add a new item to the user feed.

    Args:
        user: The username or identifier of the author (non-empty string).
        content: The text content of the feed item (non-empty string).
        item_type: Optional category/type string (default: "post").

    Returns:
        The newly created feed entry as a dict.

    Raises:
        ValueError: If user or content is empty.
    """
    if not user or not user.strip():
        raise ValueError("User cannot be empty.")
    if not content or not content.strip():
        raise ValueError("Feed item content cannot be empty.")

    entries = _load_feed()
    next_id = max((e["id"] for e in entries), default=0) + 1
    entry = {
        "id": next_id,
        "user": user.strip(),
        "content": content.strip(),
        "type": item_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    entries.append(entry)
    _save_feed(entries)
    return entry


def get_feed(user=None):
    """Return feed entries, optionally filtered by user.

    Args:
        user: Optional username to filter entries for a specific user.

    Returns:
        A list of feed entry dicts ordered by submission time.
    """
    entries = _load_feed()
    if user is not None:
        entries = [e for e in entries if e["user"] == user]
    return entries


def display_feed(user=None):
    """Print feed entries to stdout in a human-readable format.

    Args:
        user: Optional username to filter the feed.
    """
    entries = get_feed(user=user)
    if not entries:
        print("No feed items found.")
        return
    header = f"Feed for {user}" if user else "User Feed"
    print(f"{'='*40}")
    print(f"{header} ({len(entries)} item(s))")
    print(f"{'='*40}")
    for entry in entries:
        print(f"[#{entry['id']}] {entry['timestamp']} | @{entry['user']} [{entry['type']}]")
        print(f"  {entry['content']}")
    print(f"{'='*40}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args or args[0] == "view":
        user_filter = args[1] if len(args) > 1 else None
        display_feed(user=user_filter)
    elif args[0] == "add":
        if len(args) < 3:
            print("Usage: feed.py add <user> <content> [type]")
            sys.exit(1)
        item_user = args[1]
        item_content = args[2]
        item_type = args[3] if len(args) > 3 else "post"
        entry = add_feed_item(item_user, item_content, item_type)
        print(f"Feed item added (id={entry['id']}): @{entry['user']}: {entry['content']}")
    else:
        print("Usage: feed.py [view [user] | add <user> <content> [type]]")
        sys.exit(1)
