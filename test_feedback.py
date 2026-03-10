#!/usr/bin/env python3

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from feedback import collect_feedback, save_feedback, submit_feedback


class TestCollectFeedback(unittest.TestCase):

    @patch("builtins.input", side_effect=["3", "Looks good"])
    def test_valid_rating_and_comment(self, _mock):
        result = collect_feedback()
        self.assertEqual(result["rating"], 3)
        self.assertEqual(result["comment"], "Looks good")
        self.assertIn("timestamp", result)

    @patch("builtins.input", side_effect=["4", ""])
    def test_empty_comment(self, _mock):
        result = collect_feedback()
        self.assertEqual(result["rating"], 4)
        self.assertEqual(result["comment"], "")

    @patch("builtins.input", side_effect=["0", "6", "abc", "5", "Works well"])
    def test_invalid_then_valid_rating(self, _mock):
        result = collect_feedback()
        self.assertEqual(result["rating"], 5)

    @patch("builtins.input", side_effect=["2", "Fine"])
    def test_timestamp_is_present(self, _mock):
        result = collect_feedback()
        self.assertTrue(result["timestamp"])


class TestSaveFeedback(unittest.TestCase):

    def _tmp_path(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(path)  # Remove so save_feedback creates it fresh
        return path

    def test_file_created_on_first_save(self):
        path = self._tmp_path()
        try:
            save_feedback({"rating": 1, "comment": "test", "timestamp": "t1"}, path)
            self.assertTrue(os.path.exists(path))
        finally:
            os.unlink(path)

    def test_single_entry_stored(self):
        path = self._tmp_path()
        try:
            entry = {"rating": 2, "comment": "ok", "timestamp": "t2"}
            save_feedback(entry, path)
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["rating"], 2)
        finally:
            os.unlink(path)

    def test_appends_to_existing_file(self):
        path = self._tmp_path()
        try:
            save_feedback({"rating": 3, "comment": "first", "timestamp": "t3"}, path)
            save_feedback({"rating": 4, "comment": "second", "timestamp": "t4"}, path)
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[1]["comment"], "second")
        finally:
            os.unlink(path)


class TestSubmitFeedback(unittest.TestCase):

    @patch("builtins.input", side_effect=["5", "Excellent"])
    def test_submit_creates_file(self, _mock):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(path)
        try:
            with patch("feedback.FEEDBACK_FILE", path):
                submit_feedback()
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "Average"])
    def test_submit_prints_confirmation(self, _mock_input, mock_print):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(path)
        try:
            with patch("feedback.FEEDBACK_FILE", path):
                submit_feedback()
            printed = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Thank you" in s for s in printed))
        finally:
            if os.path.exists(path):
                os.unlink(path)


if __name__ == "__main__":
    unittest.main()
