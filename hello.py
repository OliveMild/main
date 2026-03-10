#!/usr/bin/env python3

from user_feed import UserFeed

if __name__ == "__main__":
    print("Hello World")

    feed = UserFeed()
    feed.add_post("alice", "Hello, this is my first post!")
    feed.add_post("bob", "Welcome to the user feed!")
    post = feed.add_post("alice", "User feeds are great!")
    feed.like_post(0)
    feed.like_post(2)
    feed.display()
