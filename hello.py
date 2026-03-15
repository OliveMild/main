#!/usr/bin/env python3

import os
import sys

if __name__ == "__main__":
    try:
        print("Hello World")
        sys.stdout.flush()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        os.close(devnull)
        sys.exit(1)
