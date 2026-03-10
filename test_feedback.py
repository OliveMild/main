#!/usr/bin/env python3
"""Unit tests for the feedback module."""

import io
import sys
import unittest

from feedback import FeedbackCollector


class TestFeedbackCollector(unittest.TestCase):
    def setUp(self):
        self.collector = FeedbackCollector()

    def test_submit_valid_feedback(self):
        entry = self.collector.submit(5, "Great app!")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "Great app!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_no_comment(self):
        entry = self.collector.submit(3)
        self.assertEqual(entry["rating"], 3)
        self.assertEqual(entry["comment"], "")

    def test_submit_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            self.collector.submit(0)

    def test_submit_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            self.collector.submit(6)

    def test_submit_invalid_rating_type(self):
        with self.assertRaises(ValueError):
            self.collector.submit("5")

    def test_get_all_empty(self):
        self.assertEqual(self.collector.get_all(), [])

    def test_get_all_returns_copy(self):
        self.collector.submit(4, "Nice")
        result = self.collector.get_all()
        result.clear()
        self.assertEqual(len(self.collector.get_all()), 1)

    def test_average_rating_no_feedback(self):
        self.assertEqual(self.collector.average_rating(), 0.0)

    def test_average_rating(self):
        self.collector.submit(4)
        self.collector.submit(2)
        self.assertAlmostEqual(self.collector.average_rating(), 3.0)

    def test_display_no_feedback(self):
        captured = io.StringIO()
        sys.stdout = captured
        try:
            self.collector.display()
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn("No feedback submitted yet.", captured.getvalue())

    def test_display_with_feedback(self):
        self.collector.submit(5, "Excellent")
        captured = io.StringIO()
        sys.stdout = captured
        try:
            self.collector.display()
        finally:
            sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Excellent", output)
        self.assertIn("5.0", output)


if __name__ == "__main__":
    unittest.main()
