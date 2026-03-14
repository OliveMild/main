#!/usr/bin/env python3


def greet(name=None):
    if name is None:
        return "Hello World"
    return f"Hello {name}"


if __name__ == "__main__":
    print(greet())

