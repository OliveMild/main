#!/usr/bin/env python3

import unittest
from hello import greet


class TestGreet(unittest.TestCase):
    def test_greet_no_name(self):
        self.assertEqual(greet(), "Hello, World!")

    def test_greet_with_name(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_greet_with_another_name(self):
        self.assertEqual(greet("Bob"), "Hello, Bob!")

    def test_greet_none_explicitly(self):
        self.assertEqual(greet(None), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
