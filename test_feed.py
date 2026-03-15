#!/usr/bin/env python3
"""Unit tests for the feed module."""

import json
import os
import tempfile
import unittest

from feed import display_feed, get_feed, post_to_feed


class TestPostToFeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)  # start without the file to test creation
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    # --- valid posts ---

    def test_post_returns_entry(self):
        entry = post_to_feed("alice", "Hello!", filepath=self.filepath)
        self.assertEqual(entry["user"], "alice")
        self.assertEqual(entry["content"], "Hello!")

    def test_post_includes_timestamp(self):
        entry = post_to_feed("alice", "Hello!", filepath=self.filepath)
        self.assertIn("timestamp", entry)

    def test_post_persists_to_file(self):
        post_to_feed("alice", "Hello!", filepath=self.filepath)
        self.assertTrue(os.path.exists(self.filepath))

    def test_post_multiple_entries_appends(self):
        post_to_feed("alice", "First post", filepath=self.filepath)
        post_to_feed("bob", "Second post", filepath=self.filepath)
        entries = get_feed(self.filepath)
        self.assertEqual(len(entries), 2)

    def test_post_strips_whitespace_from_user(self):
        entry = post_to_feed("  alice  ", "Hello!", filepath=self.filepath)
        self.assertEqual(entry["user"], "alice")

    def test_post_strips_whitespace_from_content(self):
        entry = post_to_feed("alice", "  Hello!  ", filepath=self.filepath)
        self.assertEqual(entry["content"], "Hello!")

    # --- invalid inputs ---

    def test_post_non_string_user_raises_type_error(self):
        with self.assertRaises(TypeError):
            post_to_feed(123, "Hello!", filepath=self.filepath)

    def test_post_none_user_raises_type_error(self):
        with self.assertRaises(TypeError):
            post_to_feed(None, "Hello!", filepath=self.filepath)

    def test_post_non_string_content_raises_type_error(self):
        with self.assertRaises(TypeError):
            post_to_feed("alice", 42, filepath=self.filepath)

    def test_post_empty_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            post_to_feed("", "Hello!", filepath=self.filepath)

    def test_post_whitespace_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            post_to_feed("   ", "Hello!", filepath=self.filepath)

    def test_post_empty_content_raises_value_error(self):
        with self.assertRaises(ValueError):
            post_to_feed("alice", "", filepath=self.filepath)

    def test_post_whitespace_content_raises_value_error(self):
        with self.assertRaises(ValueError):
            post_to_feed("alice", "   ", filepath=self.filepath)


class TestGetFeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_returns_empty_list_when_file_missing(self):
        self.assertEqual(get_feed(self.filepath), [])

    def test_returns_empty_list_for_corrupt_json(self):
        with open(self.filepath, "w") as f:
            f.write("not valid json{{{")
        self.assertEqual(get_feed(self.filepath), [])

    def test_returns_all_entries(self):
        post_to_feed("alice", "First", filepath=self.filepath)
        post_to_feed("bob", "Second", filepath=self.filepath)
        entries = get_feed(self.filepath)
        self.assertEqual(len(entries), 2)

    def test_entries_sorted_newest_first(self):
        post_to_feed("alice", "First", filepath=self.filepath)
        post_to_feed("bob", "Second", filepath=self.filepath)
        entries = get_feed(self.filepath)
        self.assertEqual(entries[0]["user"], "bob")
        self.assertEqual(entries[1]["user"], "alice")


class TestDisplayFeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_display_empty_feed_prints_no_posts(self, ):
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        try:
            display_feed(self.filepath)
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn("No posts yet", captured.getvalue())

    def test_display_feed_prints_entries(self):
        import io
        import sys
        post_to_feed("alice", "Hello!", filepath=self.filepath)
        captured = io.StringIO()
        sys.stdout = captured
        try:
            display_feed(self.filepath)
        finally:
            sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("alice", output)
        self.assertIn("Hello!", output)


if __name__ == "__main__":
    unittest.main()
