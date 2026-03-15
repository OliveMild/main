#!/usr/bin/env python3

from user_profile import UserProfile, UserProfileError

if __name__ == "__main__":
    print("Hello World")
    try:
        profile = UserProfile(username="world", email="world@example.com")
        print(f"User profile: {profile}")
    except UserProfileError as e:
        print(f"User profile error: {e}")
