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
    # add_feed_item
    # ------------------------------------------------------------------

    def test_add_basic_feed_item(self):
        entry = feed.add_feed_item("alice", "Hello world!")
        self.assertEqual(entry["user"], "alice")
        self.assertEqual(entry["content"], "Hello world!")
        self.assertEqual(entry["type"], "post")
        self.assertEqual(entry["id"], 1)

    def test_add_feed_item_with_type(self):
        entry = feed.add_feed_item("bob", "Shared a link", item_type="share")
        self.assertEqual(entry["type"], "share")

    def test_add_multiple_entries_increments_id(self):
        e1 = feed.add_feed_item("alice", "First post")
        e2 = feed.add_feed_item("bob", "Second post")
        self.assertEqual(e1["id"], 1)
        self.assertEqual(e2["id"], 2)

    def test_add_strips_whitespace(self):
        entry = feed.add_feed_item("  alice  ", "  padded content  ")
        self.assertEqual(entry["user"], "alice")
        self.assertEqual(entry["content"], "padded content")

    def test_add_empty_user_raises(self):
        with self.assertRaises(ValueError):
            feed.add_feed_item("", "Some content")

    def test_add_whitespace_only_user_raises(self):
        with self.assertRaises(ValueError):
            feed.add_feed_item("   ", "Some content")

    def test_add_empty_content_raises(self):
        with self.assertRaises(ValueError):
            feed.add_feed_item("alice", "")

    def test_add_whitespace_only_content_raises(self):
        with self.assertRaises(ValueError):
            feed.add_feed_item("alice", "   ")

    def test_entry_has_timestamp(self):
        entry = feed.add_feed_item("alice", "Timestamped post")
        self.assertIn("timestamp", entry)
        self.assertTrue(len(entry["timestamp"]) > 0)

    # ------------------------------------------------------------------
    # get_feed
    # ------------------------------------------------------------------

    def test_get_feed_empty(self):
        self.assertEqual(feed.get_feed(), [])

    def test_get_feed_returns_all_entries(self):
        feed.add_feed_item("alice", "A")
        feed.add_feed_item("bob", "B")
        entries = feed.get_feed()
        self.assertEqual(len(entries), 2)

    def test_get_feed_filtered_by_user(self):
        feed.add_feed_item("alice", "Alice post")
        feed.add_feed_item("bob", "Bob post")
        feed.add_feed_item("alice", "Another Alice post")
        alice_entries = feed.get_feed(user="alice")
        self.assertEqual(len(alice_entries), 2)
        for entry in alice_entries:
            self.assertEqual(entry["user"], "alice")

    def test_get_feed_filtered_nonexistent_user(self):
        feed.add_feed_item("alice", "Alice post")
        entries = feed.get_feed(user="charlie")
        self.assertEqual(entries, [])

    # ------------------------------------------------------------------
    # display_feed
    # ------------------------------------------------------------------

    def test_display_no_feed(self):
        with patch("builtins.print") as mock_print:
            feed.display_feed()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("No feed items found", output)

    def test_display_shows_entries(self):
        feed.add_feed_item("alice", "Hello from Alice", item_type="post")
        with patch("builtins.print") as mock_print:
            feed.display_feed()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("alice", output)
        self.assertIn("Hello from Alice", output)

    def test_display_filtered_by_user(self):
        feed.add_feed_item("alice", "Alice content")
        feed.add_feed_item("bob", "Bob content")
        with patch("builtins.print") as mock_print:
            feed.display_feed(user="alice")
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("alice", output)
        self.assertNotIn("Bob content", output)

    def test_display_no_items_for_user(self):
        feed.add_feed_item("alice", "Alice content")
        with patch("builtins.print") as mock_print:
            feed.display_feed(user="nobody")
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("No feed items found", output)


if __name__ == "__main__":
    unittest.main()
