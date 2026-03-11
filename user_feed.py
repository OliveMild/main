#!/usr/bin/env python3
"""User feed module for managing and displaying posts."""

from datetime import datetime, timezone


class FeedPost:
    """Represents a single post in the user feed."""

    def __init__(self, author, content):
        if not author or not author.strip():
            raise ValueError("Author must not be blank")
        if not content or not content.strip():
            raise ValueError("Content must not be blank")
        self.author = author.strip()
        self.content = content.strip()
        self.timestamp = datetime.now(timezone.utc)
        self.likes = 0

    def like(self):
        """Increment the like count for this post."""
        self.likes += 1

    def __repr__(self):
        return (
            f"FeedPost(author={self.author!r}, content={self.content!r}, "
            f"likes={self.likes}, timestamp={self.timestamp.isoformat()})"
        )


class UserFeed:
    """Manages a collection of user posts."""

    def __init__(self):
        self._posts = []

    def add_post(self, author, content):
        """Create and store a new post.

        Returns the created FeedPost.
        """
        post = FeedPost(author, content)
        self._posts.append(post)
        return post

    def get_posts(self, reverse=True):
        """Return all posts, newest first by default."""
        return list(reversed(self._posts)) if reverse else list(self._posts)

    def like_post(self, index):
        """Like a post by its position in insertion order (0-based).

        Raises IndexError for out-of-range indices.
        """
        if index < 0 or index >= len(self._posts):
            raise IndexError(f"No post at index {index}")
        self._posts[index].like()

    def display(self):
        """Pretty-print the feed to stdout."""
        posts = self.get_posts()
        count = len(posts)
        sep = "-" * 40
        print(f"{sep}\nUser Feed ({count} post{'s' if count != 1 else ''})\n{sep}")
        if not posts:
            print("  (no posts yet)")
        for post in posts:
            ts = post.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] {post.author}: {post.content}")
            if post.likes:
                print(f"  ♥ {post.likes} like{'s' if post.likes != 1 else ''}")
        print(sep)
