#!/usr/bin/env python3
"""Tests for the user feed module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feed


class TestFeedModule(unittest.TestCase):
    """Unit tests for feed.py."""

    def setUp(self):
        """Use a temporary file for feed storage during each test."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        with open(self.tmp.name, "w", encoding="utf-8") as fh:
            json.dump([], fh)
        self.patch_file = patch.object(feed, "FEED_FILE", self.tmp.name)
        self.patch_file.start()

    def tearDown(self):
        self.patch_file.stop()
        os.unlink(self.tmp.name)

    # ------------------------------------------------------------------
    # post_item
    # ------------------------------------------------------------------

    def test_post_basic_item(self):
        entry = feed.post_item("alice", "Hello, feed!")
        self.assertEqual(entry["username"], "alice")
        self.assertEqual(entry["content"], "Hello, feed!")
        self.assertEqual(entry["likes"], 0)
        self.assertEqual(entry["id"], 1)

    def test_post_multiple_items_increments_id(self):
        e1 = feed.post_item("alice", "First")
        e2 = feed.post_item("bob", "Second")
        self.assertEqual(e1["id"], 1)
        self.assertEqual(e2["id"], 2)

    def test_post_strips_whitespace(self):
        entry = feed.post_item("  alice  ", "  trimmed content  ")
        self.assertEqual(entry["username"], "alice")
        self.assertEqual(entry["content"], "trimmed content")

    def test_post_empty_username_raises(self):
        with self.assertRaises(ValueError):
            feed.post_item("", "some content")

    def test_post_whitespace_username_raises(self):
        with self.assertRaises(ValueError):
            feed.post_item("   ", "some content")

    def test_post_empty_content_raises(self):
        with self.assertRaises(ValueError):
            feed.post_item("alice", "")

    def test_post_whitespace_content_raises(self):
        with self.assertRaises(ValueError):
            feed.post_item("alice", "   ")

    def test_post_entry_has_timestamp(self):
        entry = feed.post_item("alice", "timestamped post")
        self.assertIn("timestamp", entry)
        self.assertTrue(entry["timestamp"])

    # ------------------------------------------------------------------
    # get_feed
    # ------------------------------------------------------------------

    def test_get_feed_empty(self):
        self.assertEqual(feed.get_feed(), [])

    def test_get_feed_returns_all_entries(self):
        feed.post_item("alice", "A")
        feed.post_item("bob", "B")
        entries = feed.get_feed()
        self.assertEqual(len(entries), 2)

    # ------------------------------------------------------------------
    # like_item
    # ------------------------------------------------------------------

    def test_like_item_increments_likes(self):
        entry = feed.post_item("alice", "Likeable post")
        updated = feed.like_item(entry["id"])
        self.assertEqual(updated["likes"], 1)

    def test_like_item_multiple_times(self):
        entry = feed.post_item("alice", "Very popular")
        feed.like_item(entry["id"])
        updated = feed.like_item(entry["id"])
        self.assertEqual(updated["likes"], 2)

    def test_like_nonexistent_item_raises(self):
        with self.assertRaises(ValueError):
            feed.like_item(999)

    # ------------------------------------------------------------------
    # display_feed
    # ------------------------------------------------------------------

    def test_display_empty_feed(self):
        with patch("builtins.print") as mock_print:
            feed.display_feed()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("empty", output)

    def test_display_shows_entries(self):
        feed.post_item("alice", "Hello display test")
        with patch("builtins.print") as mock_print:
            feed.display_feed()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("alice", output)
        self.assertIn("Hello display test", output)

    def test_display_shows_likes(self):
        entry = feed.post_item("alice", "Post with likes")
        feed.like_item(entry["id"])
        with patch("builtins.print") as mock_print:
            feed.display_feed()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("1 like", output)


if __name__ == "__main__":
    unittest.main()
