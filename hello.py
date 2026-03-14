#!/usr/bin/env python3
"""A simple greeting script."""


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name."""
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
