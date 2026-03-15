#!/usr/bin/env python3

from feed import DEFAULT_FILEPATH, display_feed, post_to_feed


def interact_with_feed():
    """Prompt the user to post to the feed and then display it."""
    print("\n--- Add to Feed ---")
    user = input("Your name: ").strip()
    content = input("What's on your mind? ").strip()
    try:
        post_to_feed(user, content, filepath=DEFAULT_FILEPATH)
        print("Post added!")
    except (TypeError, ValueError) as e:
        print(f"Could not add post: {e}")
    display_feed(DEFAULT_FILEPATH)


if __name__ == "__main__":
    print("Hello World")
    interact_with_feed()
