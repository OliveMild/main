#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    name = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if not name:
        name = "World"
    print(f"Hello, {name}!")
