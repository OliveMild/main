#!/usr/bin/env python3
"""Tests for the user feedback module."""

import json
import os
import tempfile
import unittest

from feedback import get_all_feedback, get_average_rating, submit_feedback


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_submit_valid_feedback(self):
        entry = submit_feedback(4, "Great app!", filepath=self.filepath)
        self.assertEqual(entry["rating"], 4)
        self.assertEqual(entry["comment"], "Great app!")
        self.assertIn("timestamp", entry)

    def test_submit_feedback_without_comment(self):
        entry = submit_feedback(3, filepath=self.filepath)
        self.assertEqual(entry["rating"], 3)
        self.assertEqual(entry["comment"], "")

    def test_submit_feedback_boundary_ratings(self):
        submit_feedback(1, filepath=self.filepath)
        submit_feedback(5, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["rating"], 1)
        self.assertEqual(entries[1]["rating"], 5)

    def test_submit_invalid_rating_zero(self):
        with self.assertRaises(ValueError):
            submit_feedback(0, filepath=self.filepath)

    def test_submit_invalid_rating_six(self):
        with self.assertRaises(ValueError):
            submit_feedback(6, filepath=self.filepath)

    def test_submit_invalid_rating_string(self):
        with self.assertRaises(ValueError):
            submit_feedback("5", filepath=self.filepath)

    def test_submit_invalid_rating_bool(self):
        with self.assertRaises(ValueError):
            submit_feedback(True, filepath=self.filepath)
        with self.assertRaises(ValueError):
            submit_feedback(False, filepath=self.filepath)

    def test_feedback_persisted_to_file(self):
        submit_feedback(2, "Needs improvement", filepath=self.filepath)
        with open(self.filepath) as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rating"], 2)

    def test_multiple_submissions_accumulate(self):
        submit_feedback(5, "Excellent", filepath=self.filepath)
        submit_feedback(3, "Okay", filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 2)


class TestGetAllFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_empty_when_no_file(self):
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(entries, [])

    def test_returns_all_entries(self):
        submit_feedback(4, filepath=self.filepath)
        submit_feedback(2, "Not great", filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 2)


class TestGetAverageRating(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_none_when_no_feedback(self):
        self.assertIsNone(get_average_rating(filepath=self.filepath))

    def test_average_single_entry(self):
        submit_feedback(4, filepath=self.filepath)
        self.assertAlmostEqual(get_average_rating(filepath=self.filepath), 4.0)

    def test_average_multiple_entries(self):
        submit_feedback(2, filepath=self.filepath)
        submit_feedback(4, filepath=self.filepath)
        self.assertAlmostEqual(get_average_rating(filepath=self.filepath), 3.0)


if __name__ == "__main__":
    unittest.main()
