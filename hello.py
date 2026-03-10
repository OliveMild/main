#!/usr/bin/env python3

from user_profile import create_profile, load_profile

if __name__ == "__main__":
    print("Hello World")
    try:
        profile = load_profile()
        print(f"Welcome back, {profile['name']}!")
    except FileNotFoundError:
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        try:
            create_profile(name, email)
            print(f"Profile created for {name}.")
        except (TypeError, ValueError) as e:
            print(f"Could not create profile: {e}")
