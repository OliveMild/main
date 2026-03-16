#!/usr/bin/env python3
import os

if __name__ == "__main__":
    name = os.environ.get("NAME", "World")
    print(f"Hello, {name}!")
