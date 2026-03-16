#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    name = arg if arg else "World"
    print(f"Hello, {name}!")
