#!/usr/bin/env python3

from feedback import submit_feedback, get_average_rating

if __name__ == "__main__":
    print("Hello World")
    submit_feedback(5, "Great application!")
    print(f"Average rating: {get_average_rating():.1f}")
