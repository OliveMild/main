#!/usr/bin/env python3
import unittest
from hello import FeedbackManager


class TestFeedbackManager(unittest.TestCase):
    def setUp(self):
        self.manager = FeedbackManager()

    def test_display_empty(self):
        self.assertEqual(self.manager.display(), "No feedback submitted yet.")

    def test_submit_and_display(self):
        self.manager.submit("Great app!", 5)
        result = self.manager.display()
        self.assertIn("[5/5]", result)
        self.assertIn("Great app!", result)
        self.assertIn("Average rating: 5/5", result)

    def test_submit_multiple_average(self):
        self.manager.submit("Great app!", 5)
        self.manager.submit("Needs work", 2)
        result = self.manager.display()
        self.assertIn("[5/5]", result)
        self.assertIn("[2/5]", result)
        self.assertIn("Average rating: 3.5/5", result)

    def test_submit_invalid_rating_too_high(self):
        with self.assertRaises(ValueError):
            self.manager.submit("Too high", 6)

    def test_submit_invalid_rating_too_low(self):
        with self.assertRaises(ValueError):
            self.manager.submit("Too low", 0)

    def test_submit_invalid_rating_non_integer(self):
        with self.assertRaises(ValueError):
            self.manager.submit("Float rating", 4.5)

    def test_submit_invalid_rating_boolean(self):
        with self.assertRaises(ValueError):
            self.manager.submit("Bool rating", True)

    def test_display_includes_timestamp(self):
        self.manager.submit("With timestamp", 3)
        result = self.manager.display()
        # Timestamps are in ISO format like 2026-03-10T11:27:43+00:00
        self.assertIn("+00:00", result)

    def test_display_numbered_entries(self):
        self.manager.submit("First", 4)
        self.manager.submit("Second", 3)
        result = self.manager.display()
        self.assertIn("1.", result)
        self.assertIn("2.", result)


if __name__ == "__main__":
    unittest.main()
