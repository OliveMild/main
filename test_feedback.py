#!/usr/bin/env python3
"""Tests for the feedback module."""

import os
import tempfile
import unittest
from unittest.mock import patch

from feedback import collect_feedback, load_feedback, save_feedback, run_feedback


class TestCollectFeedback(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "Great app!"])
    def test_collect_feedback_valid(self, mock_input):
        entry = collect_feedback()
        self.assertEqual(entry["rating"], 3)
        self.assertEqual(entry["comment"], "Great app!")
        self.assertIn("timestamp", entry)

    @patch("builtins.input", side_effect=["5", ""])
    def test_collect_feedback_no_comment(self, mock_input):
        entry = collect_feedback()
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "")

    @patch("builtins.input", side_effect=["0", "6", "abc", "2", "Good"])
    def test_collect_feedback_invalid_then_valid(self, mock_input):
        entry = collect_feedback()
        self.assertEqual(entry["rating"], 2)


class TestSaveLoadFeedback(unittest.TestCase):
    def setUp(self):
        fd, self.tmpfile = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.tmpfile)  # remove so tests start with no file

    def tearDown(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)

    def test_save_and_load_single_entry(self):
        entry = {"rating": 4, "comment": "Nice", "timestamp": "2026-01-01T00:00:00"}
        save_feedback(entry, self.tmpfile)
        loaded = load_feedback(self.tmpfile)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["rating"], 4)

    def test_save_multiple_entries(self):
        entry1 = {"rating": 3, "comment": "OK", "timestamp": "2026-01-01T00:00:00"}
        entry2 = {"rating": 5, "comment": "Excellent", "timestamp": "2026-01-02T00:00:00"}
        save_feedback(entry1, self.tmpfile)
        save_feedback(entry2, self.tmpfile)
        loaded = load_feedback(self.tmpfile)
        self.assertEqual(len(loaded), 2)

    def test_load_empty_when_no_file(self):
        result = load_feedback("/nonexistent_path/feedback.json")
        self.assertEqual(result, [])


class TestRunFeedback(unittest.TestCase):
    @patch("builtins.input", side_effect=["4", "Works well"])
    @patch("feedback.save_feedback")
    def test_run_feedback_calls_save(self, mock_save, mock_input):
        run_feedback()
        mock_save.assert_called_once()
        args = mock_save.call_args[0]
        self.assertEqual(args[0]["rating"], 4)
        self.assertEqual(args[0]["comment"], "Works well")


if __name__ == "__main__":
    unittest.main()
