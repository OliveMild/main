#!/usr/bin/env python3

import argparse


def greet(name: str = "World") -> str:
    """Return a greeting message for the given name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Greet a person by name.")
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))
