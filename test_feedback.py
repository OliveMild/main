"""Unit tests for the feedback module."""

import json
import os
import unittest
from unittest.mock import patch

from feedback import collect_feedback, load_feedback, run_feedback, save_feedback

TEST_FILE = "/tmp/test_feedback.json"


class TestCollectFeedback(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", ""])
    def test_valid_rating_no_comment(self, _mock):
        result = collect_feedback()
        self.assertEqual(result["rating"], 3)
        self.assertEqual(result["comment"], "")

    @patch("builtins.input", side_effect=["5", "Great!"])
    def test_valid_rating_with_comment(self, _mock):
        result = collect_feedback()
        self.assertEqual(result["rating"], 5)
        self.assertEqual(result["comment"], "Great!")

    @patch("builtins.input", side_effect=["0", "6", "abc", "2", ""])
    def test_invalid_ratings_then_valid(self, _mock):
        """Non-numeric and out-of-range inputs are rejected; valid input succeeds."""
        result = collect_feedback()
        self.assertEqual(result["rating"], 2)


class TestSaveAndLoadFeedback(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_load_returns_empty_list_when_no_file(self):
        self.assertEqual(load_feedback(TEST_FILE), [])

    def test_save_and_load_single_entry(self):
        entry = {"rating": 4, "comment": "Nice"}
        save_feedback(entry, TEST_FILE)
        entries = load_feedback(TEST_FILE)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], entry)

    def test_save_appends_multiple_entries(self):
        save_feedback({"rating": 1, "comment": "Bad"}, TEST_FILE)
        save_feedback({"rating": 5, "comment": "Excellent"}, TEST_FILE)
        entries = load_feedback(TEST_FILE)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1]["rating"], 5)

    def test_saved_file_is_valid_json(self):
        save_feedback({"rating": 3, "comment": ""}, TEST_FILE)
        with open(TEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)


class TestRunFeedback(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    @patch("feedback.save_feedback")
    @patch("builtins.input", side_effect=["4", "Works well"])
    def test_run_feedback_saves_entry(self, _mock_input, mock_save):
        run_feedback()
        mock_save.assert_called_once_with({"rating": 4, "comment": "Works well"})

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["4", ""])
    def test_run_feedback_prints_thank_you(self, _mock_input, mock_print):
        run_feedback()
        messages = [call.args[0] for call in mock_print.call_args_list if call.args]
        self.assertIn("Thank you for your feedback!", messages)


if __name__ == "__main__":
    unittest.main()
