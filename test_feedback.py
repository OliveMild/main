#!/usr/bin/env python3
"""Unit tests for the feedback module."""

import json
import os
import unittest

import feedback


class TestFeedback(unittest.TestCase):
    def setUp(self):
        """Remove feedback file before each test to start fresh."""
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def tearDown(self):
        """Clean up feedback file after each test."""
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def test_submit_feedback_creates_entry(self):
        entry = feedback.submit_feedback("Alice", "Great product!", 5)
        self.assertEqual(entry["user"], "Alice")
        self.assertEqual(entry["message"], "Great product!")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["id"], 1)

    def test_submit_feedback_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Bob", "Too low", 0)

    def test_submit_feedback_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Bob", "Too high", 6)

    def test_get_feedback_empty(self):
        result = feedback.get_feedback()
        self.assertEqual(result, [])

    def test_get_feedback_returns_all_entries(self):
        feedback.submit_feedback("Alice", "Good", 4)
        feedback.submit_feedback("Bob", "Excellent", 5)
        result = feedback.get_feedback()
        self.assertEqual(len(result), 2)

    def test_get_average_rating_no_entries(self):
        avg = feedback.get_average_rating()
        self.assertEqual(avg, 0.0)

    def test_get_average_rating_single_entry(self):
        feedback.submit_feedback("Alice", "Nice", 4)
        avg = feedback.get_average_rating()
        self.assertEqual(avg, 4.0)

    def test_get_average_rating_multiple_entries(self):
        feedback.submit_feedback("Alice", "Good", 4)
        feedback.submit_feedback("Bob", "Great", 2)
        avg = feedback.get_average_rating()
        self.assertEqual(avg, 3.0)

    def test_submit_feedback_increments_id(self):
        first = feedback.submit_feedback("Alice", "First", 3)
        second = feedback.submit_feedback("Bob", "Second", 4)
        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)

    def test_submit_feedback_persists_to_file(self):
        feedback.submit_feedback("Alice", "Saved", 5)
        self.assertTrue(os.path.exists(feedback.FEEDBACK_FILE))
        with open(feedback.FEEDBACK_FILE) as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["user"], "Alice")


if __name__ == "__main__":
    unittest.main()
