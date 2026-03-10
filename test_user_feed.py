#!/usr/bin/env python3
"""Unit tests for user_feed.py."""

import io
import unittest
from unittest.mock import patch

from user_feed import FeedPost, UserFeed


class TestFeedPost(unittest.TestCase):
    def test_valid_post_attributes(self):
        post = FeedPost("alice", "Hello!")
        self.assertEqual(post.author, "alice")
        self.assertEqual(post.content, "Hello!")
        self.assertEqual(post.likes, 0)
        self.assertIsNotNone(post.timestamp)

    def test_blank_author_raises(self):
        with self.assertRaises(ValueError):
            FeedPost("", "Some content")

    def test_whitespace_author_raises(self):
        with self.assertRaises(ValueError):
            FeedPost("   ", "Some content")

    def test_blank_content_raises(self):
        with self.assertRaises(ValueError):
            FeedPost("alice", "")

    def test_whitespace_content_raises(self):
        with self.assertRaises(ValueError):
            FeedPost("alice", "   ")

    def test_repr(self):
        post = FeedPost("alice", "Hi")
        self.assertIn("alice", repr(post))
        self.assertIn("Hi", repr(post))


class TestUserFeed(unittest.TestCase):
    def setUp(self):
        self.feed = UserFeed()

    def test_add_post_returns_feed_post(self):
        post = self.feed.add_post("alice", "First post")
        self.assertIsInstance(post, FeedPost)

    def test_get_posts_empty(self):
        self.assertEqual(self.feed.get_posts(), [])

    def test_get_posts_reverse_default(self):
        self.feed.add_post("alice", "First")
        self.feed.add_post("bob", "Second")
        posts = self.feed.get_posts()
        self.assertEqual(posts[0].author, "bob")
        self.assertEqual(posts[1].author, "alice")

    def test_get_posts_insertion_order(self):
        self.feed.add_post("alice", "First")
        self.feed.add_post("bob", "Second")
        posts = self.feed.get_posts(reverse=False)
        self.assertEqual(posts[0].author, "alice")
        self.assertEqual(posts[1].author, "bob")

    def test_like_post_increments_likes(self):
        self.feed.add_post("alice", "Post")
        self.feed.like_post(0)
        self.assertEqual(self.feed.get_posts(reverse=False)[0].likes, 1)

    def test_like_post_multiple_times(self):
        self.feed.add_post("alice", "Post")
        self.feed.like_post(0)
        self.feed.like_post(0)
        self.assertEqual(self.feed.get_posts(reverse=False)[0].likes, 2)

    def test_like_post_out_of_range_raises(self):
        with self.assertRaises(IndexError):
            self.feed.like_post(0)

    def test_like_post_negative_index_raises(self):
        self.feed.add_post("alice", "Post")
        with self.assertRaises(IndexError):
            self.feed.like_post(-1)

    def test_display_output_contains_author(self):
        self.feed.add_post("alice", "Hello feed!")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertIn("alice", output)
        self.assertIn("Hello feed!", output)

    def test_display_shows_like_count(self):
        self.feed.add_post("bob", "Liked post")
        self.feed.like_post(0)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertIn("1 like", output)

    def test_display_shows_plural_likes(self):
        self.feed.add_post("bob", "Popular post")
        self.feed.like_post(0)
        self.feed.like_post(0)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertIn("2 likes", output)

    def test_display_no_likes_omitted(self):
        self.feed.add_post("alice", "No likes yet")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertNotIn("\u2665", output)

    def test_display_post_count_singular(self):
        self.feed.add_post("alice", "Solo post")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertIn("1 post", output)

    def test_display_post_count_plural(self):
        self.feed.add_post("alice", "First")
        self.feed.add_post("bob", "Second")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            self.feed.display()
            output = mock_out.getvalue()
        self.assertIn("2 posts", output)

    def test_add_post_blank_author_raises(self):
        with self.assertRaises(ValueError):
            self.feed.add_post("", "Content")

    def test_add_post_blank_content_raises(self):
        with self.assertRaises(ValueError):
            self.feed.add_post("alice", "")


if __name__ == "__main__":
    unittest.main()
