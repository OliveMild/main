#!/usr/bin/env python3

import argparse
import datetime


def get_time_based_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


def greet(name=None, time_based=False):
    if time_based:
        greeting = get_time_based_greeting()
    else:
        greeting = "Hello"

    if name:
        print(f"{greeting}, {name}!")
    else:
        print(f"{greeting}, World!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a greeting message.")
    parser.add_argument("name", nargs="?", help="Name to greet")
    parser.add_argument(
        "--time", "-t",
        action="store_true",
        help="Use a time-based greeting (Good morning/afternoon/evening/night)",
    )
    args = parser.parse_args()
    greet(args.name, args.time)
