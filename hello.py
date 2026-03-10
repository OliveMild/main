#!/usr/bin/env python3

from feedback import FeedbackCollector


if __name__ == "__main__":
    print("Hello World")

    collector = FeedbackCollector()
    collector.submit(5, "Excellent first impression!")
    collector.submit(4, "Works well.")
    collector.submit(3)
    collector.display()
