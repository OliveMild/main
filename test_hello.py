#!/usr/bin/env python3

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import hello


class TestFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".json", mode="w"
        )
        self.tmp.close()
        self.original_file = hello.FEEDBACK_FILE
        hello.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        hello.FEEDBACK_FILE = self.original_file
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_load_feedback_empty(self):
        os.unlink(self.tmp.name)
        hello.FEEDBACK_FILE = self.tmp.name
        result = hello.load_feedback()
        self.assertEqual(result, [])

    def test_save_and_load_feedback(self):
        entries = [{"rating": 4, "comment": "Great!", "timestamp": "2026-01-01T00:00:00"}]
        hello.save_feedback(entries)
        loaded = hello.load_feedback()
        self.assertEqual(loaded, entries)

    def test_submit_feedback(self):
        with patch("builtins.input", side_effect=["5", "Excellent"]):
            hello.submit_feedback()
        feedback = hello.load_feedback()
        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0]["rating"], 5)
        self.assertEqual(feedback[0]["comment"], "Excellent")

    def test_submit_feedback_invalid_then_valid(self):
        with patch("builtins.input", side_effect=["0", "6", "abc", "3", ""]):
            hello.submit_feedback()
        feedback = hello.load_feedback()
        self.assertEqual(feedback[0]["rating"], 3)

    def test_view_feedback_empty(self):
        os.unlink(self.tmp.name)
        hello.FEEDBACK_FILE = self.tmp.name
        with patch("builtins.print") as mock_print:
            hello.view_feedback()
        mock_print.assert_any_call("\nNo feedback submitted yet.")

    def test_view_feedback_with_entries(self):
        entries = [
            {"rating": 5, "comment": "Awesome", "timestamp": "2026-01-01T10:00:00"},
            {"rating": 3, "comment": "", "timestamp": "2026-01-02T10:00:00"},
        ]
        hello.save_feedback(entries)
        with patch("builtins.print") as mock_print:
            hello.view_feedback()
        printed = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("4.0" in s for s in printed))

    def test_main_exit(self):
        with patch("builtins.input", return_value="3"):
            with patch("builtins.print") as mock_print:
                hello.main()
        mock_print.assert_any_call("Goodbye!")

    def test_main_invalid_choice(self):
        with patch("builtins.input", return_value="9"):
            with patch("builtins.print") as mock_print:
                hello.main()
        mock_print.assert_any_call("Invalid choice.")


if __name__ == "__main__":
    unittest.main()
