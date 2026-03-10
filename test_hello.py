"""Tests for hello.py"""
import contextlib
import io
import unittest

from hello import main


class TestMain(unittest.TestCase):
    def test_main_prints_hello_world(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        self.assertEqual(buf.getvalue(), "Hello World\n")


if __name__ == "__main__":
    unittest.main()
