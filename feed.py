#!/usr/bin/env python3
"""User feed module for posting and viewing feed items."""

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


def post_item(username, content):
    """Post a new item to the user feed.

    Args:
        username: The name of the user posting the item (non-empty string).
        content: The content of the feed item (non-empty string).

    Returns:
        The newly created feed entry as a dict.

    Raises:
        ValueError: If username or content is empty.
    """
    if not username or not username.strip():
        raise ValueError("Username cannot be empty.")
    if not content or not content.strip():
        raise ValueError("Content cannot be empty.")

    entries = _load_feed()
    next_id = max((e["id"] for e in entries), default=0) + 1
    entry = {
        "id": next_id,
        "username": username.strip(),
        "content": content.strip(),
        "likes": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    entries.append(entry)
    _save_feed(entries)
    return entry


def get_feed():
    """Return all feed entries.

    Returns:
        A list of feed entry dicts ordered by post time.
    """
    return _load_feed()


def like_item(item_id):
    """Like a feed item by its ID.

    Args:
        item_id: The integer ID of the feed item to like.

    Returns:
        The updated feed entry dict.

    Raises:
        ValueError: If no item with the given ID exists.
    """
    entries = _load_feed()
    for entry in entries:
        if entry["id"] == item_id:
            entry["likes"] += 1
            _save_feed(entries)
            return entry
    raise ValueError(f"No feed item found with id={item_id}.")


def display_feed():
    """Print all feed entries to stdout in a human-readable format."""
    entries = get_feed()
    if not entries:
        print("The feed is empty.")
        return
    print("=" * 40)
    print(f"User Feed ({len(entries)} item(s))")
    print("=" * 40)
    for entry in entries:
        print(f"[#{entry['id']}] {entry['username']}  •  {entry['timestamp']}")
        print(f"  {entry['content']}")
        like_word = "like" if entry["likes"] == 1 else "likes"
        print(f"  ♥ {entry['likes']} {like_word}")
    print("=" * 40)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args or args[0] == "view":
        display_feed()
    elif args[0] == "post":
        if len(args) < 3:
            print("Usage: feed.py post <username> <content>")
            sys.exit(1)
        entry = post_item(args[1], " ".join(args[2:]))
        print(f"Posted (id={entry['id']}): {entry['content']}")
    elif args[0] == "like":
        if len(args) < 2:
            print("Usage: feed.py like <id>")
            sys.exit(1)
        try:
            item_id = int(args[1])
        except ValueError:
            print(f"Error: id must be an integer, got '{args[1]}'")
            sys.exit(1)
        entry = like_item(item_id)
        print(f"Liked item #{entry['id']} (total likes: {entry['likes']})")
    else:
        print("Usage: feed.py [view | post <username> <content> | like <id>]")
        sys.exit(1)
