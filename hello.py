#!/usr/bin/env python3

from user_profile import UserProfile

if __name__ == "__main__":
    print("Hello World")
    try:
        profile = UserProfile("alice", "alice@example.com")
        print(profile.display())
    except ValueError as e:
        print(f"Error: {e}")
