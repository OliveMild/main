#!/usr/bin/env python3
"""Tests for the user feedback module."""

import os
import unittest

import feedback


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        # Remove the feedback file before each test to start fresh
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def tearDown(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def test_submit_creates_entry(self):
        entry = feedback.submit_feedback("Alice", "Great app!", 5)
        self.assertEqual(entry["user"], "Alice")
        self.assertEqual(entry["message"], "Great app!")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["id"], 1)

    def test_submit_increments_id(self):
        feedback.submit_feedback("Alice", "First", 4)
        second = feedback.submit_feedback("Bob", "Second", 3)
        self.assertEqual(second["id"], 2)

    def test_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Alice", "Bad rating", 0)

    def test_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("Alice", "Bad rating", 6)

    def test_valid_boundary_ratings(self):
        low = feedback.submit_feedback("Alice", "Min rating", 1)
        high = feedback.submit_feedback("Bob", "Max rating", 5)
        self.assertEqual(low["rating"], 1)
        self.assertEqual(high["rating"], 5)


class TestGetFeedback(unittest.TestCase):
    def setUp(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def tearDown(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def test_empty_when_no_entries(self):
        self.assertEqual(feedback.get_feedback(), [])

    def test_returns_all_entries(self):
        feedback.submit_feedback("Alice", "Good", 4)
        feedback.submit_feedback("Bob", "Great", 5)
        entries = feedback.get_feedback()
        self.assertEqual(len(entries), 2)


class TestGetAverageRating(unittest.TestCase):
    def setUp(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def tearDown(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def test_zero_when_no_entries(self):
        self.assertEqual(feedback.get_average_rating(), 0.0)

    def test_average_single_entry(self):
        feedback.submit_feedback("Alice", "Decent", 4)
        self.assertEqual(feedback.get_average_rating(), 4.0)

    def test_average_multiple_entries(self):
        feedback.submit_feedback("Alice", "Good", 4)
        feedback.submit_feedback("Bob", "Great", 5)
        feedback.submit_feedback("Charlie", "OK", 3)
        self.assertAlmostEqual(feedback.get_average_rating(), 4.0)


class TestPersistence(unittest.TestCase):
    def setUp(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def tearDown(self):
        if os.path.exists(feedback.FEEDBACK_FILE):
            os.remove(feedback.FEEDBACK_FILE)

    def test_entries_persist_to_file(self):
        feedback.submit_feedback("Alice", "Persistent", 5)
        self.assertTrue(os.path.exists(feedback.FEEDBACK_FILE))

    def test_entries_reload_from_file(self):
        feedback.submit_feedback("Alice", "Reload me", 3)
        # Re-read from disk
        entries = feedback.get_feedback()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["user"], "Alice")


if __name__ == "__main__":
    unittest.main()
