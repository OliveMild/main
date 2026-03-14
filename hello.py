#!/usr/bin/env python3
"""Simple greeting module."""


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name. Defaults to "World" if no name is provided."""
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
