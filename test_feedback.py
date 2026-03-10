#!/usr/bin/env python3
"""Unit tests for the feedback module."""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import feedback as fb


class TestSubmitFeedback(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for each test to avoid side-effects
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self._orig_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name
        # Start with an empty file
        os.unlink(self.tmp.name)

    def tearDown(self):
        fb.FEEDBACK_FILE = self._orig_file
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_submit_valid_entry(self):
        entry = fb.submit_feedback(5, "Great!")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "Great!")

    def test_submit_persists_to_file(self):
        fb.submit_feedback(3, "Average")
        with open(fb.FEEDBACK_FILE, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rating"], 3)
        self.assertEqual(data[0]["comment"], "Average")

    def test_submit_multiple_entries(self):
        fb.submit_feedback(5, "Excellent")
        fb.submit_feedback(1, "Poor")
        entries = fb.view_feedback()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["rating"], 5)
        self.assertEqual(entries[1]["rating"], 1)

    def test_submit_rating_boundary_low(self):
        entry = fb.submit_feedback(1, "Minimum rating")
        self.assertEqual(entry["rating"], 1)

    def test_submit_rating_boundary_high(self):
        entry = fb.submit_feedback(5, "Maximum rating")
        self.assertEqual(entry["rating"], 5)

    def test_submit_invalid_rating_type_float(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback(3.5, "Float rating")

    def test_submit_invalid_rating_type_string(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback("5", "String rating")

    def test_submit_invalid_rating_bool_true(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback(True, "Boolean rating")

    def test_submit_invalid_rating_bool_false(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback(False, "Boolean rating")

    def test_submit_rating_too_low(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(0, "Too low")

    def test_submit_rating_too_high(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(6, "Too high")

    def test_submit_empty_comment(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(3, "")

    def test_submit_whitespace_only_comment(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(3, "   ")

    def test_submit_comment_not_string(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback(3, 42)

    def test_submit_comment_none(self):
        with self.assertRaises(TypeError):
            fb.submit_feedback(3, None)


class TestViewFeedback(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self._orig_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name
        os.unlink(self.tmp.name)

    def tearDown(self):
        fb.FEEDBACK_FILE = self._orig_file
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_view_empty_when_no_file(self):
        self.assertEqual(fb.view_feedback(), [])

    def test_view_returns_submitted_entries(self):
        fb.submit_feedback(4, "Good")
        fb.submit_feedback(2, "Needs work")
        entries = fb.view_feedback()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["comment"], "Good")
        self.assertEqual(entries[1]["comment"], "Needs work")


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self._orig_file = fb.FEEDBACK_FILE
        fb.FEEDBACK_FILE = self.tmp.name
        os.unlink(self.tmp.name)

    def tearDown(self):
        fb.FEEDBACK_FILE = self._orig_file
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_cli_submit(self):
        with patch("builtins.print") as mock_print:
            fb._main(["submit", "5", "Great", "work"])
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]
        self.assertIn("5", output)

    def test_cli_view_no_entries(self):
        with patch("builtins.print") as mock_print:
            fb._main(["view"])
        mock_print.assert_called_once()
        self.assertIn("No feedback", mock_print.call_args[0][0])

    def test_cli_view_with_entries(self):
        fb.submit_feedback(3, "Average")
        with patch("builtins.print") as mock_print:
            fb._main(["view"])
        self.assertTrue(mock_print.called)

    def test_cli_submit_invalid_rating(self):
        with self.assertRaises(SystemExit):
            fb._main(["submit", "abc", "comment"])

    def test_cli_unknown_command(self):
        with self.assertRaises(SystemExit):
            fb._main(["unknown"])

    def test_cli_no_args(self):
        with self.assertRaises(SystemExit):
            fb._main([])


if __name__ == "__main__":
    unittest.main()
