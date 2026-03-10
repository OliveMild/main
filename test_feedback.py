#!/usr/bin/env python3
"""Tests for the feedback module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feedback as fb


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        """Use a temporary file for feedback storage during tests."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        self.original_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        fb.FEEDBACK_FILE = self.original_file
        os.unlink(self.tmp.name)

    def test_submit_feedback_stores_entry(self):
        entry = fb.submit_feedback("Alice", "Great app!")
        self.assertEqual(entry["user"], "Alice")
        self.assertEqual(entry["message"], "Great app!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_persists_to_file(self):
        fb.submit_feedback("Bob", "Needs improvement.")
        stored = fb.get_all_feedback()
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["user"], "Bob")

    def test_multiple_feedback_entries(self):
        fb.submit_feedback("Alice", "Loves it!")
        fb.submit_feedback("Bob", "Pretty good.")
        stored = fb.get_all_feedback()
        self.assertEqual(len(stored), 2)

    def test_empty_user_name_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback("", "Some feedback")

    def test_whitespace_user_name_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback("   ", "Some feedback")

    def test_empty_message_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback("Alice", "")

    def test_whitespace_message_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback("Alice", "   ")

    def test_strips_whitespace(self):
        entry = fb.submit_feedback("  Alice  ", "  Hello!  ")
        self.assertEqual(entry["user"], "Alice")
        self.assertEqual(entry["message"], "Hello!")


class TestGetAllFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        self.original_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        fb.FEEDBACK_FILE = self.original_file
        os.unlink(self.tmp.name)

    def test_returns_empty_list_when_no_feedback(self):
        # Write empty JSON array so the file is valid but empty
        with open(fb.FEEDBACK_FILE, "w") as f:
            json.dump([], f)
        self.assertEqual(fb.get_all_feedback(), [])

    def test_returns_empty_list_when_file_missing(self):
        os.unlink(fb.FEEDBACK_FILE)
        # Point to a non-existent path
        fb.FEEDBACK_FILE = self.tmp.name + "_missing"
        self.assertEqual(fb.get_all_feedback(), [])
        fb.FEEDBACK_FILE = self.tmp.name
        # Recreate so tearDown can clean up properly
        open(self.tmp.name, "w").close()

    def test_returns_empty_list_when_file_corrupted(self):
        with open(fb.FEEDBACK_FILE, "w") as f:
            f.write("not valid json{{")
        self.assertEqual(fb.get_all_feedback(), [])


class TestCollectFeedbackFromUser(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        self.original_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        fb.FEEDBACK_FILE = self.original_file
        os.unlink(self.tmp.name)

    def test_collect_feedback_from_user_success(self):
        with patch("builtins.input", side_effect=["Carol", "Wonderful!"]):
            with patch("builtins.print") as mock_print:
                fb.collect_feedback_from_user()
        stored = fb.get_all_feedback()
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["user"], "Carol")
        # Confirm thank-you message was printed
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Carol", output)

    def test_collect_feedback_from_user_strips_whitespace_input(self):
        with patch("builtins.input", side_effect=["  Dave  ", "  Works great!  "]):
            with patch("builtins.print"):
                fb.collect_feedback_from_user()
        stored = fb.get_all_feedback()
        self.assertEqual(stored[0]["user"], "Dave")
        self.assertEqual(stored[0]["message"], "Works great!")
        with patch("builtins.input", side_effect=["", "Some message"]):
            with patch("builtins.print") as mock_print:
                fb.collect_feedback_from_user()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Error", output)


if __name__ == "__main__":
    unittest.main()
