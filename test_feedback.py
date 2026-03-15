#!/usr/bin/env python3
"""Tests for the user feedback module."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from feedback import collect_feedback, save_feedback, submit_feedback


class TestCollectFeedback(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "Great app!"])
    def test_collect_feedback_returns_dict(self, _mock_input):
        result = collect_feedback()
        self.assertEqual(result["rating"], 3)
        self.assertEqual(result["comment"], "Great app!")
        self.assertIn("timestamp", result)

    @patch("builtins.input", side_effect=["5", ""])
    def test_collect_feedback_empty_comment(self, _mock_input):
        result = collect_feedback()
        self.assertEqual(result["rating"], 5)
        self.assertEqual(result["comment"], "")

    @patch("builtins.input", side_effect=["0", "6", "abc", "2", "Works well"])
    def test_collect_feedback_invalid_then_valid_rating(self, _mock_input):
        result = collect_feedback()
        self.assertEqual(result["rating"], 2)


class TestSaveFeedback(unittest.TestCase):
    def test_save_creates_file(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        os.unlink(tmp_path)  # remove so save_feedback creates it fresh
        try:
            feedback = {"rating": 4, "comment": "Nice", "timestamp": "2026-01-01T00:00:00"}
            save_feedback(feedback, filepath=tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["rating"], 4)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save_appends_to_existing(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as tmp:
            json.dump([{"rating": 1, "comment": "Old", "timestamp": "2025-01-01T00:00:00"}], tmp)
            tmp_path = tmp.name

        try:
            feedback = {"rating": 5, "comment": "New", "timestamp": "2026-01-01T00:00:00"}
            save_feedback(feedback, filepath=tmp_path)
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[1]["rating"], 5)
        finally:
            os.unlink(tmp_path)


class TestSubmitFeedback(unittest.TestCase):
    @patch("builtins.input", side_effect=["4", "Good job"])
    def test_submit_feedback(self, _mock_input):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name
        os.unlink(tmp_path)

        try:
            with patch("feedback.save_feedback") as mock_save:
                result = submit_feedback()

            self.assertEqual(result["rating"], 4)
            self.assertEqual(result["comment"], "Good job")
            mock_save.assert_called_once_with(result)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
