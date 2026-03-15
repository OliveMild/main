#!/usr/bin/env python3
"""Tests for the feedback module."""

import json
import os
import tempfile
import unittest

from feedback import get_average_rating, load_feedback, submit_feedback


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)  # Remove so load_feedback starts fresh
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_submit_valid_rating(self):
        submit_feedback(3, filepath=self.filepath)
        entries = load_feedback(self.filepath)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["rating"], 3)

    def test_submit_with_comment(self):
        submit_feedback(5, comment="Great!", filepath=self.filepath)
        entries = load_feedback(self.filepath)
        self.assertEqual(entries[0]["comment"], "Great!")

    def test_submit_multiple(self):
        submit_feedback(1, filepath=self.filepath)
        submit_feedback(5, filepath=self.filepath)
        entries = load_feedback(self.filepath)
        self.assertEqual(len(entries), 2)

    def test_rating_too_low(self):
        with self.assertRaises(ValueError):
            submit_feedback(0, filepath=self.filepath)

    def test_rating_too_high(self):
        with self.assertRaises(ValueError):
            submit_feedback(6, filepath=self.filepath)

    def test_rating_not_integer(self):
        with self.assertRaises(TypeError):
            submit_feedback("3", filepath=self.filepath)

    def test_boolean_rating_rejected(self):
        with self.assertRaises(TypeError):
            submit_feedback(True, filepath=self.filepath)

    def test_boundary_rating_1(self):
        submit_feedback(1, filepath=self.filepath)
        entries = load_feedback(self.filepath)
        self.assertEqual(entries[0]["rating"], 1)

    def test_boundary_rating_5(self):
        submit_feedback(5, filepath=self.filepath)
        entries = load_feedback(self.filepath)
        self.assertEqual(entries[0]["rating"], 5)


class TestLoadFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_load_missing_file(self):
        self.assertEqual(load_feedback(self.filepath), [])

    def test_load_corrupt_file(self):
        with open(self.filepath, "w") as f:
            f.write("not valid json")
        self.assertEqual(load_feedback(self.filepath), [])

    def test_load_returns_entries(self):
        with open(self.filepath, "w") as f:
            json.dump([{"rating": 4, "comment": "ok", "timestamp": "t"}], f)
        entries = load_feedback(self.filepath)
        self.assertEqual(entries[0]["rating"], 4)


class TestGetAverageRating(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.unlink(self.filepath)

    def test_average_empty(self):
        self.assertEqual(get_average_rating(self.filepath), 0.0)

    def test_average_single(self):
        submit_feedback(4, filepath=self.filepath)
        self.assertAlmostEqual(get_average_rating(self.filepath), 4.0)

    def test_average_multiple(self):
        submit_feedback(2, filepath=self.filepath)
        submit_feedback(4, filepath=self.filepath)
        self.assertAlmostEqual(get_average_rating(self.filepath), 3.0)


if __name__ == "__main__":
    unittest.main()
