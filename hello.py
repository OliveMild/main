#!/usr/bin/env python3

from feedback import DEFAULT_FILEPATH, get_average_rating, submit_feedback


def collect_feedback():
    """Prompt the user for a rating and optional comment, then save it."""
    print("\nWe'd love your feedback!")
    while True:
        try:
            rating = int(input("Rate your experience (1–5): "))
            if rating < 1 or rating > 5:
                raise ValueError
            break
        except (TypeError, ValueError):
            print("Please enter a whole number between 1 and 5.")
    comment = input("Any comments? (press Enter to skip): ").strip()
    submit_feedback(rating, comment=comment, filepath=DEFAULT_FILEPATH)
    avg = get_average_rating(filepath=DEFAULT_FILEPATH)
    if avg is not None:
        print(f"Thanks! Overall average rating: {avg:.1f}/5")
    else:
        print("Thanks for your feedback!")


if __name__ == "__main__":
    print("Hello World")
    collect_feedback()
