#!/usr/bin/env python3
"""Tests for the user feedback module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feedback


class TestFeedback(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for feedback storage during tests
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        self.original_file = feedback.FEEDBACK_FILE
        feedback.FEEDBACK_FILE = self.tmp.name
        # Start each test with an empty feedback store
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        feedback.FEEDBACK_FILE = self.original_file
        os.unlink(self.tmp.name)

    # --- submit_feedback ---

    def test_submit_feedback_basic(self):
        entry = feedback.submit_feedback("Great app!")
        self.assertEqual(entry["message"], "Great app!")
        self.assertIn("timestamp", entry)
        self.assertNotIn("rating", entry)

    def test_submit_feedback_with_rating(self):
        entry = feedback.submit_feedback("Nice work", rating=5)
        self.assertEqual(entry["rating"], 5)

    def test_submit_feedback_strips_whitespace(self):
        entry = feedback.submit_feedback("  Needs improvement  ")
        self.assertEqual(entry["message"], "Needs improvement")

    def test_submit_feedback_empty_message_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("")

    def test_submit_feedback_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("   ")

    def test_submit_feedback_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Good", rating=6)
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Good", rating=0)

    def test_submit_feedback_persists(self):
        feedback.submit_feedback("First")
        feedback.submit_feedback("Second")
        entries = feedback.get_all_feedback()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["message"], "First")
        self.assertEqual(entries[1]["message"], "Second")

    # --- get_all_feedback ---

    def test_get_all_feedback_empty(self):
        self.assertEqual(feedback.get_all_feedback(), [])

    def test_get_all_feedback_returns_all(self):
        feedback.submit_feedback("A")
        feedback.submit_feedback("B", rating=3)
        entries = feedback.get_all_feedback()
        self.assertEqual(len(entries), 2)

    # --- load_feedback when file missing ---

    def test_load_feedback_missing_file(self):
        os.unlink(self.tmp.name)
        result = feedback.load_feedback()
        self.assertEqual(result, [])
        # Restore tmp file so tearDown doesn't fail
        with open(self.tmp.name, "w") as f:
            json.dump([], f)


if __name__ == "__main__":
    unittest.main()
