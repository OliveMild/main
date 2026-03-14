#!/usr/bin/env python3
"""A simple Hello World script."""


def greet(name="World"):
    """Return a greeting message for the given name."""
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
