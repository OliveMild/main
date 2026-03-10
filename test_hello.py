"""Tests for the greet function in hello.py."""

from hello import greet


def test_greet_default():
    assert greet() == "Hello, World!"


def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_returns_string():
    assert isinstance(greet(), str)
