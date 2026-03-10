#!/usr/bin/env python3
"""Hello World application.

This module provides a simple greeting application that prints
a greeting message to standard output.
"""

import sys


def greet(name="World"):
    """Return a greeting message for the given name.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting string.
    """
    return f"Hello {name}"


def main():
    """Print a greeting to standard output.

    Reads an optional name from command-line arguments.
    If no name is provided, defaults to "World".
    """
    name = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "World"
    print(greet(name))


if __name__ == "__main__":
    main()
