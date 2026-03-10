#!/usr/bin/env python3
"""Tests for the feedback module."""

import unittest

from feedback import FeedbackError, FeedbackManager


class TestFeedbackManagerSubmit(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_submit_valid_feedback(self):
        entry = self.manager.submit("Great app!", 5)
        self.assertEqual(entry["message"], "Great app!")
        self.assertEqual(entry["rating"], 5)
        self.assertIn("timestamp", entry)

    def test_submit_stores_entry(self):
        self.manager.submit("Nice work", 4)
        self.assertEqual(len(self.manager.get_all()), 1)

    def test_submit_multiple_entries(self):
        self.manager.submit("First comment", 3)
        self.manager.submit("Second comment", 5)
        self.assertEqual(len(self.manager.get_all()), 2)

    def test_submit_strips_whitespace_from_message(self):
        entry = self.manager.submit("  Hello  ", 3)
        self.assertEqual(entry["message"], "Hello")

    def test_submit_empty_message_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("", 3)

    def test_submit_whitespace_only_message_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("   ", 3)

    def test_submit_rating_below_range_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Good", 0)

    def test_submit_rating_above_range_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Good", 6)

    def test_submit_non_integer_rating_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Good", 3.5)  # type: ignore[arg-type]

    def test_submit_boundary_rating_1(self):
        entry = self.manager.submit("Minimum rating", 1)
        self.assertEqual(entry["rating"], 1)

    def test_submit_boundary_rating_5(self):
        entry = self.manager.submit("Maximum rating", 5)
        self.assertEqual(entry["rating"], 5)


class TestFeedbackManagerGetAll(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_get_all_empty(self):
        self.assertEqual(self.manager.get_all(), [])

    def test_get_all_returns_copy(self):
        self.manager.submit("Test", 3)
        result = self.manager.get_all()
        result.clear()
        self.assertEqual(len(self.manager.get_all()), 1)


class TestFeedbackManagerAverageRating(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_average_rating_no_feedback(self):
        self.assertEqual(self.manager.average_rating(), 0.0)

    def test_average_rating_single_entry(self):
        self.manager.submit("Only one", 4)
        self.assertEqual(self.manager.average_rating(), 4.0)

    def test_average_rating_multiple_entries(self):
        self.manager.submit("First", 2)
        self.manager.submit("Second", 4)
        self.assertEqual(self.manager.average_rating(), 3.0)


class TestFeedbackManagerDisplay(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_display_no_feedback(self):
        self.assertIn("No feedback", self.manager.display())

    def test_display_with_feedback(self):
        self.manager.submit("Looks good", 4)
        output = self.manager.display()
        self.assertIn("Looks good", output)
        self.assertIn("4/5", output)
        self.assertIn("Average rating", output)

    def test_display_lists_all_entries(self):
        self.manager.submit("First", 3)
        self.manager.submit("Second", 5)
        output = self.manager.display()
        self.assertIn("First", output)
        self.assertIn("Second", output)


if __name__ == "__main__":
    unittest.main()
