#!/usr/bin/env python3
"""Tests for the user feedback module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feedback as fb


class TestFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.orig = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name
        # Start with an empty file
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        fb.FEEDBACK_FILE = self.orig
        os.unlink(self.tmp.name)

    def test_submit_feedback_stores_entry(self):
        entry = fb.submit_feedback(4, "Nice!")
        self.assertEqual(entry["rating"], 4)
        self.assertEqual(entry["comment"], "Nice!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_no_comment(self):
        entry = fb.submit_feedback(3)
        self.assertEqual(entry["comment"], "")

    def test_load_feedback_returns_list(self):
        fb.submit_feedback(5, "Excellent")
        data = fb.load_feedback()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rating"], 5)

    def test_get_average_rating(self):
        fb.submit_feedback(4)
        fb.submit_feedback(2)
        self.assertAlmostEqual(fb.get_average_rating(), 3.0)

    def test_get_average_rating_empty(self):
        self.assertEqual(fb.get_average_rating(), 0.0)

    def test_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(0)
        with self.assertRaises(ValueError):
            fb.submit_feedback(6)
        with self.assertRaises(ValueError):
            fb.submit_feedback("good")


if __name__ == "__main__":
    unittest.main()
