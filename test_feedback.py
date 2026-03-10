#!/usr/bin/env python3
"""Unit tests for the feedback module."""

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
        os.unlink(self.tmp.name)  # start without the file so we test creation
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    # --- valid submissions ---

    def test_submit_valid_rating_returns_entry(self):
        entry = submit_feedback(3, filepath=self.filepath)
        self.assertEqual(entry["rating"], 3)

    def test_submit_includes_comment(self):
        entry = submit_feedback(4, comment="Great!", filepath=self.filepath)
        self.assertEqual(entry["comment"], "Great!")

    def test_submit_includes_timestamp(self):
        entry = submit_feedback(5, filepath=self.filepath)
        self.assertIn("timestamp", entry)

    def test_submit_persists_to_file(self):
        submit_feedback(2, filepath=self.filepath)
        self.assertTrue(os.path.exists(self.filepath))

    def test_submit_multiple_entries_appends(self):
        submit_feedback(1, filepath=self.filepath)
        submit_feedback(5, filepath=self.filepath)
        entries = get_all_feedback(self.filepath)
        self.assertEqual(len(entries), 2)

    def test_submit_boundary_rating_1(self):
        entry = submit_feedback(1, filepath=self.filepath)
        self.assertEqual(entry["rating"], 1)

    def test_submit_boundary_rating_5(self):
        entry = submit_feedback(5, filepath=self.filepath)
        self.assertEqual(entry["rating"], 5)

    # --- invalid ratings ---

    def test_submit_rating_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            submit_feedback(0, filepath=self.filepath)

    def test_submit_rating_six_raises_value_error(self):
        with self.assertRaises(ValueError):
            submit_feedback(6, filepath=self.filepath)

    def test_submit_float_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            submit_feedback(3.0, filepath=self.filepath)

    def test_submit_string_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            submit_feedback("3", filepath=self.filepath)

    def test_submit_bool_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            submit_feedback(True, filepath=self.filepath)

    def test_submit_none_rating_raises_type_error(self):
        with self.assertRaises(TypeError):
            submit_feedback(None, filepath=self.filepath)


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

    def test_returns_empty_list_when_file_missing(self):
        self.assertEqual(get_all_feedback(self.filepath), [])

    def test_returns_empty_list_for_corrupt_json(self):
        with open(self.filepath, "w") as f:
            f.write("not valid json{{{")
        self.assertEqual(get_all_feedback(self.filepath), [])

    def test_returns_all_submitted_entries(self):
        submit_feedback(3, "ok", filepath=self.filepath)
        submit_feedback(5, "great", filepath=self.filepath)
        entries = get_all_feedback(self.filepath)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["rating"], 3)
        self.assertEqual(entries[1]["rating"], 5)


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

    def test_returns_none_when_no_entries(self):
        self.assertIsNone(get_average_rating(self.filepath))

    def test_single_entry_average_equals_rating(self):
        submit_feedback(4, filepath=self.filepath)
        self.assertEqual(get_average_rating(self.filepath), 4.0)

    def test_multiple_entries_correct_average(self):
        submit_feedback(2, filepath=self.filepath)
        submit_feedback(4, filepath=self.filepath)
        self.assertAlmostEqual(get_average_rating(self.filepath), 3.0)

    def test_average_is_float(self):
        submit_feedback(3, filepath=self.filepath)
        self.assertIsInstance(get_average_rating(self.filepath), float)


if __name__ == "__main__":
    unittest.main()
