#!/usr/bin/env python3
import unittest

from hello import greet


class TestGreet(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greet(), "Hello World")

    def test_custom_name(self):
        self.assertEqual(greet("Alice"), "Hello Alice")

    def test_empty_string(self):
        self.assertEqual(greet(""), "Hello ")


if __name__ == "__main__":
    unittest.main()
