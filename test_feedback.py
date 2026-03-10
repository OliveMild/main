#!/usr/bin/env python3

import unittest
from feedback import submit_feedback, get_average_rating, _feedback_entries


class TestFeedback(unittest.TestCase):
    def setUp(self):
        _feedback_entries.clear()

    def test_submit_feedback_with_comment(self):
        submit_feedback(5, "Great application!")
        self.assertEqual(len(_feedback_entries), 1)
        self.assertEqual(_feedback_entries[0]["rating"], 5)
        self.assertEqual(_feedback_entries[0]["comment"], "Great application!")

    def test_submit_feedback_without_comment(self):
        submit_feedback(3)
        self.assertEqual(len(_feedback_entries), 1)
        self.assertEqual(_feedback_entries[0]["rating"], 3)
        self.assertIsNone(_feedback_entries[0]["comment"])

    def test_get_average_rating(self):
        submit_feedback(5, "Great application!")
        submit_feedback(3)
        self.assertEqual(get_average_rating(), 4.0)

    def test_get_average_rating_no_feedback(self):
        self.assertEqual(get_average_rating(), 0.0)

    def test_get_average_rating_single(self):
        submit_feedback(4)
        self.assertEqual(get_average_rating(), 4.0)

    def test_submit_feedback_invalid_rating_type(self):
        with self.assertRaises(TypeError):
            submit_feedback("five")

    def test_submit_feedback_invalid_rating_range(self):
        with self.assertRaises(ValueError):
            submit_feedback(6)
        with self.assertRaises(ValueError):
            submit_feedback(0)


if __name__ == "__main__":
    unittest.main()
