#!/usr/bin/env python3
"""Greeting module providing a simple hello-world API."""

import argparse


def greet(name: str) -> str:
    """Return a greeting string for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting string of the form ``"Hello, <name>!"``.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))
