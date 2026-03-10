#!/usr/bin/env python3
"""Unit tests for the feedback module."""

import unittest

from feedback import FeedbackError, FeedbackManager


class TestFeedbackManagerSubmit(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_submit_valid_entry(self):
        self.manager.submit("Great app!", 5)
        entries = self.manager.get_all()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["message"], "Great app!")
        self.assertEqual(entries[0]["rating"], 5)

    def test_submit_boundary_rating_one(self):
        self.manager.submit("Minimal rating", 1)
        self.assertEqual(self.manager.get_all()[0]["rating"], 1)

    def test_submit_boundary_rating_five(self):
        self.manager.submit("Max rating", 5)
        self.assertEqual(self.manager.get_all()[0]["rating"], 5)

    def test_submit_multiple_entries(self):
        self.manager.submit("First", 3)
        self.manager.submit("Second", 4)
        self.assertEqual(len(self.manager.get_all()), 2)

    def test_submit_empty_message_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("", 3)

    def test_submit_whitespace_message_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("   ", 3)

    def test_submit_rating_zero_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", 0)

    def test_submit_rating_six_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", 6)

    def test_submit_negative_rating_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", -1)

    def test_submit_float_rating_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", 3.0)

    def test_submit_bool_rating_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", True)

    def test_submit_string_rating_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit("Valid message", "5")

    def test_submit_none_message_raises(self):
        with self.assertRaises(FeedbackError):
            self.manager.submit(None, 3)

    def test_entry_has_timestamp(self):
        self.manager.submit("Check timestamp", 4)
        entry = self.manager.get_all()[0]
        self.assertIn("timestamp", entry)
        self.assertTrue(entry["timestamp"].endswith("+00:00"))


class TestFeedbackManagerGetAll(unittest.TestCase):
    def test_get_all_returns_copy(self):
        manager = FeedbackManager()
        manager.submit("Entry", 3)
        entries = manager.get_all()
        entries.clear()
        self.assertEqual(len(manager.get_all()), 1)

    def test_get_all_empty(self):
        manager = FeedbackManager()
        self.assertEqual(manager.get_all(), [])


class TestFeedbackManagerAverageRating(unittest.TestCase):
    def test_average_no_entries(self):
        manager = FeedbackManager()
        self.assertEqual(manager.average_rating(), 0.0)

    def test_average_single_entry(self):
        manager = FeedbackManager()
        manager.submit("Only one", 4)
        self.assertEqual(manager.average_rating(), 4.0)

    def test_average_multiple_entries(self):
        manager = FeedbackManager()
        manager.submit("A", 5)
        manager.submit("B", 3)
        self.assertAlmostEqual(manager.average_rating(), 4.0)


class TestFeedbackManagerDisplay(unittest.TestCase):
    def test_display_no_entries(self):
        manager = FeedbackManager()
        self.assertIn("No feedback", manager.display())

    def test_display_contains_message(self):
        manager = FeedbackManager()
        manager.submit("Great app!", 5)
        output = manager.display()
        self.assertIn("Great app!", output)

    def test_display_contains_rating(self):
        manager = FeedbackManager()
        manager.submit("Good", 4)
        output = manager.display()
        self.assertIn("[4/5]", output)

    def test_display_contains_average(self):
        manager = FeedbackManager()
        manager.submit("First", 5)
        manager.submit("Second", 3)
        output = manager.display()
        self.assertIn("Average rating:", output)
        self.assertIn("4.0", output)


if __name__ == "__main__":
    unittest.main()
