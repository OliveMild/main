#!/usr/bin/env python3
"""A simple greeting module."""


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting string of the form "Hello {name}".
    """
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
