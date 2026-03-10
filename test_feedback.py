import json
import os
import tempfile
import unittest

import feedback as fb


class TestFeedback(unittest.TestCase):
    def setUp(self):
        # Use a temporary file so tests are isolated
        self._orig = fb.FEEDBACK_FILE
        fd, self._tmp = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self._tmp)  # Remove so load_feedback sees a missing file by default
        fb.FEEDBACK_FILE = self._tmp

    def tearDown(self):
        fb.FEEDBACK_FILE = self._orig
        if os.path.exists(self._tmp):
            os.remove(self._tmp)

    def test_load_feedback_empty_when_no_file(self):
        self.assertEqual(fb.load_feedback(), [])

    def test_submit_and_load_feedback(self):
        fb.submit_feedback(4, "Nice")
        entries = fb.load_feedback()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["rating"], 4)
        self.assertEqual(entries[0]["comment"], "Nice")

    def test_submit_multiple_entries(self):
        fb.submit_feedback(5, "Excellent")
        fb.submit_feedback(3)
        entries = fb.load_feedback()
        self.assertEqual(len(entries), 2)

    def test_get_average_rating(self):
        fb.submit_feedback(5)
        fb.submit_feedback(3)
        self.assertAlmostEqual(fb.get_average_rating(), 4.0)

    def test_get_average_rating_empty(self):
        self.assertEqual(fb.get_average_rating(), 0.0)

    def test_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(0)
        with self.assertRaises(ValueError):
            fb.submit_feedback(6)
        with self.assertRaises(ValueError):
            fb.submit_feedback("five")

    def test_boolean_rating_rejected(self):
        with self.assertRaises(ValueError):
            fb.submit_feedback(True)

    def test_load_feedback_handles_corrupt_file(self):
        with open(self._tmp, "w") as f:
            f.write("not valid json")
        self.assertEqual(fb.load_feedback(), [])


if __name__ == "__main__":
    unittest.main()
