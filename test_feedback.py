"""Tests for the user feedback feature."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import feedback


class TestSubmitFeedback(unittest.TestCase):
    """Tests for submit_feedback()."""

    def setUp(self):
        # Redirect FEEDBACK_FILE to a temporary file for each test
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.write("[]")
        self.tmp.close()
        self.original_file = feedback.FEEDBACK_FILE
        feedback.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        feedback.FEEDBACK_FILE = self.original_file
        os.unlink(self.tmp.name)

    def test_submit_valid_feedback(self):
        entry = feedback.submit_feedback(5, "Great app!")
        self.assertEqual(entry["rating"], 5)
        self.assertEqual(entry["comment"], "Great app!")
        self.assertIn("timestamp", entry)

    def test_submit_stores_to_file(self):
        feedback.submit_feedback(3, "It's okay.")
        with open(self.tmp.name, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rating"], 3)

    def test_submit_multiple_entries(self):
        feedback.submit_feedback(4, "Good")
        feedback.submit_feedback(2, "Needs improvement")
        entries = feedback.view_feedback()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["rating"], 4)
        self.assertEqual(entries[0]["comment"], "Good")
        self.assertEqual(entries[1]["rating"], 2)
        self.assertEqual(entries[1]["comment"], "Needs improvement")

    def test_submit_strips_whitespace(self):
        entry = feedback.submit_feedback(4, "  nice  ")
        self.assertEqual(entry["comment"], "nice")

    def test_submit_invalid_rating_low(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(0, "Bad")

    def test_submit_invalid_rating_high(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(6, "Too high")

    def test_submit_invalid_rating_type(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback("five", "Not an int")

    def test_submit_empty_comment(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(3, "")

    def test_submit_whitespace_only_comment(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(3, "   ")

    def test_submit_non_string_comment(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(3, 123)


class TestViewFeedback(unittest.TestCase):
    """Tests for view_feedback()."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.write("[]")
        self.tmp.close()
        self.original_file = feedback.FEEDBACK_FILE
        feedback.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        feedback.FEEDBACK_FILE = self.original_file
        if self.tmp and os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_view_empty(self):
        # Remove the tmp file to simulate no prior feedback file
        os.unlink(self.tmp.name)
        self.tmp = None  # prevent double-unlink in tearDown
        entries = feedback.view_feedback()
        self.assertEqual(entries, [])

    def test_view_returns_all_entries(self):
        feedback.submit_feedback(5, "Excellent")
        feedback.submit_feedback(1, "Terrible")
        entries = feedback.view_feedback()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["rating"], 5)
        self.assertEqual(entries[1]["rating"], 1)


class TestCLI(unittest.TestCase):
    """Tests for the CLI interface via main()."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.write("[]")
        self.tmp.close()
        self.original_file = feedback.FEEDBACK_FILE
        feedback.FEEDBACK_FILE = self.tmp.name

    def tearDown(self):
        feedback.FEEDBACK_FILE = self.original_file
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_submit_via_cli(self):
        with patch("sys.argv", ["feedback.py", "submit", "4", "Works well"]):
            from io import StringIO
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                feedback.main()
                self.assertIn("Feedback submitted", mock_out.getvalue())

    def test_view_via_cli_empty(self):
        with patch("sys.argv", ["feedback.py", "view"]):
            from io import StringIO
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                feedback.main()
                self.assertIn("No feedback submitted yet", mock_out.getvalue())

    def test_unknown_command_exits(self):
        with patch("sys.argv", ["feedback.py", "delete"]):
            with self.assertRaises(SystemExit):
                feedback.main()

    def test_no_args_exits(self):
        with patch("sys.argv", ["feedback.py"]):
            with self.assertRaises(SystemExit):
                feedback.main()

    def test_invalid_rating_via_cli_exits(self):
        with patch("sys.argv", ["feedback.py", "submit", "abc", "Some comment"]):
            with self.assertRaises(SystemExit):
                feedback.main()


if __name__ == "__main__":
    unittest.main()
