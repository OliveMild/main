#!/usr/bin/env python3


def greet(name=None):
    if name:
        return f"Hello {name}"
    return "Hello World"


if __name__ == "__main__":
    print(greet())
