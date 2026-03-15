#!/usr/bin/env python3
"""User feed module for managing and displaying user posts."""

from datetime import datetime


class FeedPost:
    """Represents a single post in the user feed."""

    def __init__(self, author: str, content: str):
        self.author = author
        self.content = content
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.author}: {self.content}"


class UserFeed:
    """Manages a feed of user posts."""

    def __init__(self):
        self._posts: list[FeedPost] = []

    def add_post(self, author: str, content: str) -> FeedPost:
        """Add a new post to the feed."""
        post = FeedPost(author, content)
        self._posts.append(post)
        return post

    def get_posts(self) -> list[FeedPost]:
        """Return all posts in reverse chronological order."""
        return list(reversed(self._posts))

    def display(self) -> None:
        """Print the feed to stdout."""
        posts = self.get_posts()
        if not posts:
            print("No posts in the feed yet.")
            return
        print(f"--- User Feed ({len(posts)} post{'s' if len(posts) != 1 else ''}) ---")
        for post in posts:
            print(post)
