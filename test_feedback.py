#!/usr/bin/env python3
"""Tests for the user feedback module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feedback


class TestFeedbackModule(unittest.TestCase):
    """Unit tests for feedback.py."""

    def setUp(self):
        """Use a temporary file for feedback storage during each test."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        # Seed with empty list so the file is valid JSON
        with open(self.tmp.name, "w", encoding="utf-8") as fh:
            json.dump([], fh)
        self.patch_file = patch.object(feedback, "FEEDBACK_FILE", self.tmp.name)
        self.patch_file.start()

    def tearDown(self):
        self.patch_file.stop()
        os.unlink(self.tmp.name)

    # ------------------------------------------------------------------
    # submit_feedback
    # ------------------------------------------------------------------

    def test_submit_basic_feedback(self):
        entry = feedback.submit_feedback("Great app!")
        self.assertEqual(entry["message"], "Great app!")
        self.assertIsNone(entry["rating"])
        self.assertEqual(entry["id"], 1)

    def test_submit_feedback_with_rating(self):
        entry = feedback.submit_feedback("Awesome", rating=5)
        self.assertEqual(entry["rating"], 5)

    def test_submit_multiple_entries_increments_id(self):
        e1 = feedback.submit_feedback("First")
        e2 = feedback.submit_feedback("Second")
        self.assertEqual(e1["id"], 1)
        self.assertEqual(e2["id"], 2)

    def test_submit_strips_whitespace(self):
        entry = feedback.submit_feedback("  padded  ")
        self.assertEqual(entry["message"], "padded")

    def test_submit_empty_message_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("")

    def test_submit_whitespace_only_message_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("   ")

    def test_submit_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("msg", rating=0)
        with self.assertRaises(ValueError):
            feedback.submit_feedback("msg", rating=6)

    def test_submit_valid_rating_boundaries(self):
        e1 = feedback.submit_feedback("low", rating=1)
        e2 = feedback.submit_feedback("high", rating=5)
        self.assertEqual(e1["rating"], 1)
        self.assertEqual(e2["rating"], 5)

    # ------------------------------------------------------------------
    # get_feedback
    # ------------------------------------------------------------------

    def test_get_feedback_empty(self):
        self.assertEqual(feedback.get_feedback(), [])

    def test_get_feedback_returns_all_entries(self):
        feedback.submit_feedback("A")
        feedback.submit_feedback("B")
        entries = feedback.get_feedback()
        self.assertEqual(len(entries), 2)

    # ------------------------------------------------------------------
    # display_feedback
    # ------------------------------------------------------------------

    def test_display_no_feedback(self):
        with patch("builtins.print") as mock_print:
            feedback.display_feedback()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("No feedback submitted yet", output)

    def test_display_shows_entries(self):
        feedback.submit_feedback("Hello feedback", rating=4)
        with patch("builtins.print") as mock_print:
            feedback.display_feedback()
        output = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Hello feedback", output)
        self.assertIn("4/5", output)


if __name__ == "__main__":
    unittest.main()
