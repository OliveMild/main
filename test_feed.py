#!/usr/bin/env python3
"""Tests for the user feed module."""

import os
import tempfile
import unittest

from feed import add_post, get_feed, get_user_posts


class TestAddPost(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_add_post_returns_entry(self):
        post = add_post("alice", "Hello, world!", filepath=self.filepath)
        self.assertEqual(post["username"], "alice")
        self.assertEqual(post["content"], "Hello, world!")
        self.assertIn("timestamp", post)

    def test_add_post_strips_whitespace(self):
        post = add_post("  bob  ", "  My post  ", filepath=self.filepath)
        self.assertEqual(post["username"], "bob")
        self.assertEqual(post["content"], "My post")

    def test_add_post_empty_username_raises(self):
        with self.assertRaises(ValueError):
            add_post("", "Some content", filepath=self.filepath)

    def test_add_post_whitespace_username_raises(self):
        with self.assertRaises(ValueError):
            add_post("   ", "Some content", filepath=self.filepath)

    def test_add_post_empty_content_raises(self):
        with self.assertRaises(ValueError):
            add_post("alice", "", filepath=self.filepath)

    def test_add_post_whitespace_content_raises(self):
        with self.assertRaises(ValueError):
            add_post("alice", "   ", filepath=self.filepath)

    def test_multiple_posts_accumulate(self):
        add_post("alice", "First post", filepath=self.filepath)
        add_post("bob", "Second post", filepath=self.filepath)
        feed = get_feed(filepath=self.filepath)
        self.assertEqual(len(feed), 2)


class TestGetFeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_empty_feed_when_no_file(self):
        feed = get_feed(filepath=self.filepath)
        self.assertEqual(feed, [])

    def test_feed_sorted_newest_first(self):
        add_post("alice", "Older post", filepath=self.filepath)
        add_post("bob", "Newer post", filepath=self.filepath)
        feed = get_feed(filepath=self.filepath)
        self.assertEqual(len(feed), 2)
        self.assertGreaterEqual(feed[0]["timestamp"], feed[1]["timestamp"])

    def test_feed_contains_all_posts(self):
        add_post("alice", "Post 1", filepath=self.filepath)
        add_post("alice", "Post 2", filepath=self.filepath)
        add_post("bob", "Post 3", filepath=self.filepath)
        feed = get_feed(filepath=self.filepath)
        self.assertEqual(len(feed), 3)


class TestGetUserPosts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_no_posts_for_unknown_user(self):
        add_post("alice", "Post by alice", filepath=self.filepath)
        posts = get_user_posts("bob", filepath=self.filepath)
        self.assertEqual(posts, [])

    def test_returns_only_user_posts(self):
        add_post("alice", "Alice post 1", filepath=self.filepath)
        add_post("bob", "Bob post", filepath=self.filepath)
        add_post("alice", "Alice post 2", filepath=self.filepath)
        posts = get_user_posts("alice", filepath=self.filepath)
        self.assertEqual(len(posts), 2)
        for post in posts:
            self.assertEqual(post["username"], "alice")

    def test_user_posts_sorted_newest_first(self):
        add_post("alice", "First", filepath=self.filepath)
        add_post("alice", "Second", filepath=self.filepath)
        posts = get_user_posts("alice", filepath=self.filepath)
        self.assertGreaterEqual(posts[0]["timestamp"], posts[1]["timestamp"])

    def test_empty_feed_returns_empty_list(self):
        posts = get_user_posts("alice", filepath=self.filepath)
        self.assertEqual(posts, [])


if __name__ == "__main__":
    unittest.main()
