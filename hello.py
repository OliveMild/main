#!/usr/bin/env python3

import sys


if __name__ == "__main__":
    try:
        print("Hello World")
        sys.stdout.flush()
    except BrokenPipeError:
        sys.exit(1)
