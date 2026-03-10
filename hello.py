#!/usr/bin/env python3
import argparse


def greet(name: str = "World") -> str:
    """Return a greeting message for the given name.

    The format is 'Hello <name>' with no trailing punctuation.
    """
    return f"Hello {name}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Greet someone by name.")
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name of the person to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))
