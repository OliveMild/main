#!/usr/bin/env python3
"""hello module: prints a greeting message to stdout."""


def greet():
    """Return the greeting message.

    Returns:
        str: The greeting string "Hello World".
    """
    return "Hello World"


if __name__ == "__main__":
    print(greet())
