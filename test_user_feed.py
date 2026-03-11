#!/usr/bin/env python3
"""Unit tests for the user_feed module."""

import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from user_feed import FeedPost, UserFeed


class TestFeedPost(unittest.TestCase):

    def test_creates_post_with_valid_inputs(self):
        post = FeedPost("alice", "Hello, world!")
        self.assertEqual(post.author, "alice")
        self.assertEqual(post.content, "Hello, world!")
        self.assertEqual(post.likes, 0)

    def test_strips_whitespace_from_author_and_content(self):
        post = FeedPost("  bob  ", "  Some content  ")
        self.assertEqual(post.author, "bob")
        self.assertEqual(post.content, "Some content")

    def test_raises_on_blank_author(self):
        with self.assertRaises(ValueError):
            FeedPost("", "content")
        with self.assertRaises(ValueError):
            FeedPost("   ", "content")

    def test_raises_on_blank_content(self):
        with self.assertRaises(ValueError):
            FeedPost("alice", "")
        with self.assertRaises(ValueError):
            FeedPost("alice", "   ")

    def test_like_increments_count(self):
        post = FeedPost("alice", "Hello")
        post.like()
        self.assertEqual(post.likes, 1)
        post.like()
        self.assertEqual(post.likes, 2)

    def test_timestamp_is_utc(self):
        post = FeedPost("alice", "Hello")
        self.assertEqual(post.timestamp.tzinfo, timezone.utc)

    def test_repr(self):
        post = FeedPost("alice", "Hello")
        self.assertIn("alice", repr(post))
        self.assertIn("Hello", repr(post))


class TestUserFeed(unittest.TestCase):

    def setUp(self):
        self.feed = UserFeed()

    def test_new_feed_has_no_posts(self):
        self.assertEqual(self.feed.get_posts(), [])

    def test_add_post_returns_feed_post(self):
        post = self.feed.add_post("alice", "Hello!")
        self.assertIsInstance(post, FeedPost)

    def test_get_posts_returns_newest_first_by_default(self):
        self.feed.add_post("alice", "First")
        self.feed.add_post("bob", "Second")
        posts = self.feed.get_posts()
        self.assertEqual(posts[0].author, "bob")
        self.assertEqual(posts[1].author, "alice")

    def test_get_posts_insertion_order_when_reverse_false(self):
        self.feed.add_post("alice", "First")
        self.feed.add_post("bob", "Second")
        posts = self.feed.get_posts(reverse=False)
        self.assertEqual(posts[0].author, "alice")
        self.assertEqual(posts[1].author, "bob")

    def test_like_post_increments_likes(self):
        self.feed.add_post("alice", "Hello!")
        self.feed.like_post(0)
        self.assertEqual(self.feed.get_posts(reverse=False)[0].likes, 1)

    def test_like_post_raises_on_out_of_range(self):
        with self.assertRaises(IndexError):
            self.feed.like_post(0)
        self.feed.add_post("alice", "Hello!")
        with self.assertRaises(IndexError):
            self.feed.like_post(1)
        with self.assertRaises(IndexError):
            self.feed.like_post(-1)

    def test_display_empty_feed(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.feed.display()
        output = buf.getvalue()
        self.assertIn("0 posts", output)
        self.assertIn("no posts yet", output)

    def test_display_single_post(self):
        import io
        from contextlib import redirect_stdout
        self.feed.add_post("alice", "Hello, world!")
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.feed.display()
        output = buf.getvalue()
        self.assertIn("1 post", output)
        self.assertIn("alice", output)
        self.assertIn("Hello, world!", output)

    def test_display_post_with_likes(self):
        import io
        from contextlib import redirect_stdout
        self.feed.add_post("alice", "Hello!")
        self.feed.like_post(0)
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.feed.display()
        output = buf.getvalue()
        self.assertIn("1 like", output)

    def test_display_multiple_posts(self):
        import io
        from contextlib import redirect_stdout
        self.feed.add_post("alice", "First post")
        self.feed.add_post("bob", "Second post")
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.feed.display()
        output = buf.getvalue()
        self.assertIn("2 posts", output)
        self.assertIn("alice", output)
        self.assertIn("bob", output)


if __name__ == "__main__":
    unittest.main()
