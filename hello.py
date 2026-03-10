#!/usr/bin/env python3

from feedback import submit_feedback, get_average_rating


if __name__ == "__main__":
    print("Hello World")

    submit_feedback(5, "Great application!")
    submit_feedback(4, "Works well.")
    submit_feedback(3)

    avg = get_average_rating()
    print(f"Average rating: {avg:.1f}")
