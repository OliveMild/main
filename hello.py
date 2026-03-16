#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "World"
    print(f"Hello, {name}!")
