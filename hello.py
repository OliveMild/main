#!/usr/bin/env python3


def greet(name="World"):
    """Return a greeting string for the given name.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting string in the form "Hello, {name}!".
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet())
