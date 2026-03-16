#!/usr/bin/env python3

import argparse


def greet(name=None):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a greeting message.")
    parser.add_argument("name", nargs="?", help="Name to greet")
    args = parser.parse_args()
    greet(args.name)
