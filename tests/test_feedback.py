"""Tests for the feedback module."""

import importlib
import sys
import unittest


def _fresh_feedback():
    """Return a freshly-imported feedback module with an empty store."""
    if "feedback" in sys.modules:
        del sys.modules["feedback"]
    return importlib.import_module("feedback")


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        self.feedback = _fresh_feedback()

    def test_submit_integer_rating(self):
        self.feedback.submit_feedback(5)
        self.assertEqual(len(self.feedback._feedback_store), 1)
        self.assertEqual(self.feedback._feedback_store[0]["rating"], 5)

    def test_submit_float_rating(self):
        self.feedback.submit_feedback(3.5)
        self.assertEqual(self.feedback._feedback_store[0]["rating"], 3.5)

    def test_submit_with_comment(self):
        self.feedback.submit_feedback(4, comment="Great!")
        entry = self.feedback._feedback_store[0]
        self.assertEqual(entry["rating"], 4)
        self.assertEqual(entry["comment"], "Great!")

    def test_submit_without_comment_defaults_to_none(self):
        self.feedback.submit_feedback(3)
        self.assertIsNone(self.feedback._feedback_store[0]["comment"])

    def test_submit_multiple_entries(self):
        self.feedback.submit_feedback(1)
        self.feedback.submit_feedback(2)
        self.feedback.submit_feedback(3)
        self.assertEqual(len(self.feedback._feedback_store), 3)

    def test_submit_string_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.feedback.submit_feedback("5")

    def test_submit_none_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.feedback.submit_feedback(None)

    def test_submit_list_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.feedback.submit_feedback([5])

    def test_submit_bool_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.feedback.submit_feedback(True)

    def test_type_error_message_mentions_type(self):
        with self.assertRaises(TypeError) as ctx:
            self.feedback.submit_feedback("bad")
        self.assertIn("str", str(ctx.exception))


class TestGetAverageRating(unittest.TestCase):
    def setUp(self):
        self.feedback = _fresh_feedback()

    def test_empty_store_returns_zero(self):
        self.assertEqual(self.feedback.get_average_rating(), 0.0)

    def test_single_entry_average_equals_rating(self):
        self.feedback.submit_feedback(4)
        self.assertEqual(self.feedback.get_average_rating(), 4.0)

    def test_multiple_entries_correct_average(self):
        self.feedback.submit_feedback(2)
        self.feedback.submit_feedback(4)
        self.assertEqual(self.feedback.get_average_rating(), 3.0)

    def test_float_ratings_average(self):
        self.feedback.submit_feedback(1.5)
        self.feedback.submit_feedback(2.5)
        self.assertAlmostEqual(self.feedback.get_average_rating(), 2.0)

    def test_returns_float(self):
        self.feedback.submit_feedback(5)
        self.assertIsInstance(self.feedback.get_average_rating(), float)


if __name__ == "__main__":
    unittest.main()
