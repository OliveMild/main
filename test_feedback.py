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
        """Set up a temporary file for feedback storage during tests."""
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.orig_feedback_file = feedback.FEEDBACK_FILE
        feedback.FEEDBACK_FILE = self.tmp.name
        # Start with an empty feedback file
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        """Restore original feedback file path and clean up temp file."""
        feedback.FEEDBACK_FILE = self.orig_feedback_file
        os.unlink(self.tmp.name)

    def test_submit_feedback_stores_entry(self):
        entry = feedback.submit_feedback("Alice", 5, "Great app!")
        self.assertEqual(entry["name"], "Alice")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "Great app!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_persists_to_file(self):
        feedback.submit_feedback("Bob", 4, "Good job")
        entries = feedback.list_feedback()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["name"], "Bob")

    def test_submit_multiple_feedback_entries(self):
        feedback.submit_feedback("Alice", 5, "Excellent!")
        feedback.submit_feedback("Bob", 3, "Average")
        entries = feedback.list_feedback()
        self.assertEqual(len(entries), 2)

    def test_submit_feedback_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Carol", 0, "Bad rating")

    def test_submit_feedback_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Dave", 6, "Out of range")

    def test_submit_feedback_invalid_rating_non_integer(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Eve", 3.5, "Float rating")

    def test_list_feedback_empty(self):
        entries = feedback.list_feedback()
        self.assertEqual(entries, [])

    def test_get_average_rating_no_feedback(self):
        result = feedback.get_average_rating()
        self.assertIsNone(result)

    def test_get_average_rating_single_entry(self):
        feedback.submit_feedback("Alice", 4, "Nice")
        avg = feedback.get_average_rating()
        self.assertEqual(avg, 4.0)

    def test_get_average_rating_multiple_entries(self):
        feedback.submit_feedback("Alice", 4, "Nice")
        feedback.submit_feedback("Bob", 2, "Needs work")
        avg = feedback.get_average_rating()
        self.assertEqual(avg, 3.0)

    def test_load_feedback_missing_file(self):
        os.unlink(self.tmp.name)
        result = feedback.load_feedback()
        self.assertEqual(result, [])
        # Restore for tearDown
        with open(self.tmp.name, "w") as f:
            json.dump([], f)


if __name__ == "__main__":
    unittest.main()
