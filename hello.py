#!/usr/bin/env python3
"""Simple greeting module."""


def greet(name=None):
    """Return a greeting string for the given name."""
    if name is None:
        return "Hello World"
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
