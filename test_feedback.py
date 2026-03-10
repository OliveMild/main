#!/usr/bin/env python3
"""Unit tests for feedback.py."""

import json
import os
import tempfile
import unittest

from feedback import get_all_feedback, get_average_rating, submit_feedback


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)  # start with no file
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_valid_rating_min(self):
        submit_feedback(1, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["rating"], 1)

    def test_valid_rating_max(self):
        submit_feedback(5, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(entries[0]["rating"], 5)

    def test_valid_rating_with_comment(self):
        submit_feedback(4, comment="Great!", filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(entries[0]["comment"], "Great!")

    def test_default_comment_is_empty_string(self):
        submit_feedback(3, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(entries[0]["comment"], "")

    def test_entry_has_timestamp(self):
        submit_feedback(3, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertIn("timestamp", entries[0])
        self.assertTrue(entries[0]["timestamp"])

    def test_invalid_rating_zero(self):
        with self.assertRaises(ValueError):
            submit_feedback(0, filepath=self.filepath)

    def test_invalid_rating_six(self):
        with self.assertRaises(ValueError):
            submit_feedback(6, filepath=self.filepath)

    def test_invalid_rating_negative(self):
        with self.assertRaises(ValueError):
            submit_feedback(-1, filepath=self.filepath)

    def test_invalid_rating_string(self):
        with self.assertRaises(ValueError):
            submit_feedback("5", filepath=self.filepath)

    def test_invalid_rating_float(self):
        with self.assertRaises(ValueError):
            submit_feedback(3.0, filepath=self.filepath)

    def test_invalid_rating_bool(self):
        with self.assertRaises(ValueError):
            submit_feedback(True, filepath=self.filepath)

    def test_accumulates_multiple_entries(self):
        submit_feedback(1, filepath=self.filepath)
        submit_feedback(2, filepath=self.filepath)
        submit_feedback(3, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 3)

    def test_persists_to_disk(self):
        submit_feedback(5, comment="Saved", filepath=self.filepath)
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data[0]["rating"], 5)
        self.assertEqual(data[0]["comment"], "Saved")


class TestGetAllFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_returns_empty_list_when_no_file(self):
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(entries, [])

    def test_returns_all_entries(self):
        submit_feedback(2, filepath=self.filepath)
        submit_feedback(4, filepath=self.filepath)
        entries = get_all_feedback(filepath=self.filepath)
        self.assertEqual(len(entries), 2)


class TestGetAverageRating(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_returns_none_when_empty(self):
        result = get_average_rating(filepath=self.filepath)
        self.assertIsNone(result)

    def test_average_single_entry(self):
        submit_feedback(4, filepath=self.filepath)
        self.assertEqual(get_average_rating(filepath=self.filepath), 4.0)

    def test_average_multiple_entries(self):
        submit_feedback(1, filepath=self.filepath)
        submit_feedback(5, filepath=self.filepath)
        self.assertEqual(get_average_rating(filepath=self.filepath), 3.0)

    def test_average_returns_float(self):
        submit_feedback(3, filepath=self.filepath)
        result = get_average_rating(filepath=self.filepath)
        self.assertIsInstance(result, float)


if __name__ == "__main__":
    unittest.main()
