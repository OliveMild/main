#!/usr/bin/env python3
"""Tests for the feedback module."""

import json
import os
import tempfile
import unittest

from feedback import get_average_rating, get_feedback, submit_feedback


class TestFeedback(unittest.TestCase):
    def setUp(self):
        # Use a temporary file so tests are isolated
        self.tmpfile = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmpfile.close()
        os.unlink(self.tmpfile.name)  # remove so it starts empty

    def tearDown(self):
        if os.path.exists(self.tmpfile.name):
            os.unlink(self.tmpfile.name)

    def test_submit_feedback_creates_entry(self):
        entry = submit_feedback(5, "Great!", filepath=self.tmpfile.name)
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "Great!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_stored(self):
        submit_feedback(3, "Okay", filepath=self.tmpfile.name)
        entries = get_feedback(filepath=self.tmpfile.name)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["rating"], 3)

    def test_multiple_submissions(self):
        submit_feedback(4, "Good", filepath=self.tmpfile.name)
        submit_feedback(2, "Needs work", filepath=self.tmpfile.name)
        entries = get_feedback(filepath=self.tmpfile.name)
        self.assertEqual(len(entries), 2)

    def test_invalid_rating_low(self):
        with self.assertRaises(ValueError):
            submit_feedback(0, filepath=self.tmpfile.name)

    def test_invalid_rating_high(self):
        with self.assertRaises(ValueError):
            submit_feedback(6, filepath=self.tmpfile.name)

    def test_invalid_rating_type(self):
        with self.assertRaises(ValueError):
            submit_feedback("five", filepath=self.tmpfile.name)

    def test_average_rating_no_entries(self):
        avg = get_average_rating(filepath=self.tmpfile.name)
        self.assertIsNone(avg)

    def test_average_rating(self):
        submit_feedback(4, filepath=self.tmpfile.name)
        submit_feedback(2, filepath=self.tmpfile.name)
        avg = get_average_rating(filepath=self.tmpfile.name)
        self.assertAlmostEqual(avg, 3.0)

    def test_empty_comment_allowed(self):
        entry = submit_feedback(3, filepath=self.tmpfile.name)
        self.assertEqual(entry["comment"], "")

    def test_comment_stripped(self):
        entry = submit_feedback(3, "  hello  ", filepath=self.tmpfile.name)
        self.assertEqual(entry["comment"], "hello")

    def test_get_feedback_empty(self):
        entries = get_feedback(filepath=self.tmpfile.name)
        self.assertEqual(entries, [])


if __name__ == "__main__":
    unittest.main()
