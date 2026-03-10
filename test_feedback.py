#!/usr/bin/env python3
"""Tests for the user feedback module."""

import unittest
from feedback import Feedback, FeedbackManager


class TestFeedback(unittest.TestCase):
    def test_valid_feedback(self):
        f = Feedback("Alice", "Great!", 5)
        self.assertEqual(f.user, "Alice")
        self.assertEqual(f.message, "Great!")
        self.assertEqual(f.rating, 5)

    def test_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            Feedback("Alice", "Bad", 0)

    def test_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            Feedback("Alice", "Bad", 6)

    def test_str_representation(self):
        f = Feedback("Bob", "Nice", 4)
        self.assertIn("Bob", str(f))
        self.assertIn("Nice", str(f))
        self.assertIn("4/5", str(f))


class TestFeedbackManager(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_add_feedback(self):
        f = self.manager.add_feedback("Alice", "Excellent!", 5)
        self.assertIsInstance(f, Feedback)
        self.assertEqual(len(self.manager.get_all_feedback()), 1)

    def test_get_all_feedback(self):
        self.manager.add_feedback("Alice", "Good", 4)
        self.manager.add_feedback("Bob", "Okay", 3)
        feedbacks = self.manager.get_all_feedback()
        self.assertEqual(len(feedbacks), 2)

    def test_average_rating_empty(self):
        self.assertEqual(self.manager.get_average_rating(), 0.0)

    def test_average_rating(self):
        self.manager.add_feedback("Alice", "Good", 4)
        self.manager.add_feedback("Bob", "Okay", 2)
        self.assertAlmostEqual(self.manager.get_average_rating(), 3.0)

    def test_display_feedback_empty(self):
        # No error when empty
        self.manager.display_feedback()

    def test_display_feedback(self):
        self.manager.add_feedback("Alice", "Great!", 5)
        # Should not raise
        self.manager.display_feedback()


if __name__ == "__main__":
    unittest.main()
