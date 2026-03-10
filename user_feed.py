#!/usr/bin/env python3
"""User feed module: create posts, like them, and display the feed."""

from datetime import datetime, timezone


class FeedPost:
    """A single post in the user feed."""

    def __init__(self, author: str, content: str) -> None:
        if not author or not author.strip():
            raise ValueError("author must not be blank")
        if not content or not content.strip():
            raise ValueError("content must not be blank")
        self.author = author
        self.content = content
        self.timestamp = datetime.now(timezone.utc)
        self.likes = 0

    def __repr__(self) -> str:
        return (
            f"FeedPost(author={self.author!r}, content={self.content!r}, "
            f"likes={self.likes})"
        )


class UserFeed:
    """A chronological collection of feed posts."""

    def __init__(self) -> None:
        self._posts: list[FeedPost] = []

    def add_post(self, author: str, content: str) -> FeedPost:
        """Create and store a new post; return the new FeedPost."""
        post = FeedPost(author, content)
        self._posts.append(post)
        return post

    def get_posts(self, reverse: bool = True) -> list[FeedPost]:
        """Return posts in reverse-chronological order by default."""
        return list(reversed(self._posts)) if reverse else list(self._posts)

    def like_post(self, index: int) -> None:
        """Increment likes on the post at *insertion* index (not display order)."""
        if index < 0 or index >= len(self._posts):
            raise IndexError(f"no post at index {index}")
        self._posts[index].likes += 1

    def display(self) -> None:
        """Pretty-print the feed to stdout."""
        separator = "-" * 40
        posts = self.get_posts()
        print(separator)
        print(f"User Feed ({len(posts)} post{'s' if len(posts) != 1 else ''})")
        print(separator)
        for post in posts:
            ts = post.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] {post.author}: {post.content}")
            if post.likes:
                like_word = "like" if post.likes == 1 else "likes"
                print(f"  \u2665 {post.likes} {like_word}")
        print(separator)
