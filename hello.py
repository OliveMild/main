#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    name = (sys.argv[1:2] or [""])[0].strip()
    if not name:
        name = "World"
    print(f"Hello, {name}!")
