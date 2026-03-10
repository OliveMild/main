#!/usr/bin/env python3


def greet(name: str = "World") -> str:
    """Return a greeting string."""
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())
