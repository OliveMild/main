#!/usr/bin/env python3
"""User feed module for creating and viewing user feed posts."""

import json
import os
from datetime import datetime, timezone

FEED_FILE = "feed.json"


def _load_feed(filepath=FEED_FILE):
    """Load existing feed posts from file."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_feed(posts, filepath=FEED_FILE):
    """Save feed posts to file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)


def add_post(username, content, filepath=FEED_FILE):
    """Add a new post to the user feed.

    Args:
        username: The name of the user creating the post.
        content: The text content of the post.
        filepath: Path to the feed storage file.

    Returns:
        The new post as a dict.

    Raises:
        ValueError: If username or content is empty.
    """
    if not username.strip():
        raise ValueError("Username must not be empty.")
    if not content.strip():
        raise ValueError("Post content must not be empty.")

    post = {
        "username": username.strip(),
        "content": content.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    posts = _load_feed(filepath)
    posts.append(post)
    _save_feed(posts, filepath)
    return post


def get_feed(filepath=FEED_FILE):
    """Return all posts in the feed, newest first.

    Args:
        filepath: Path to the feed storage file.

    Returns:
        List of post dicts sorted by timestamp descending.
    """
    posts = _load_feed(filepath)
    return sorted(posts, key=lambda p: p["timestamp"], reverse=True)


def get_user_posts(username, filepath=FEED_FILE):
    """Return all posts by a specific user, newest first.

    Args:
        username: The username to filter posts by.
        filepath: Path to the feed storage file.

    Returns:
        List of post dicts for the given user, sorted by timestamp descending.
    """
    posts = _load_feed(filepath)
    user_posts = [p for p in posts if p["username"] == username]
    return sorted(user_posts, key=lambda p: p["timestamp"], reverse=True)


if __name__ == "__main__":
    print("User Feed Module")
    print("Add posts by calling add_post(username, content).")
    print("View feed by calling get_feed().")
