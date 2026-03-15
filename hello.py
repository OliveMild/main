#!/usr/bin/env python3

from feedback import submit_feedback, get_average_rating

if __name__ == "__main__":
    print("Hello World")
    try:
        rating = int(input("Please rate your experience (1-5): "))
    except ValueError:
        print("Invalid input: please enter a number between 1 and 5")
    else:
        comment = input("Any comments? (press Enter to skip): ")
        try:
            submit_feedback(rating, comment)
            avg = get_average_rating()
            print(f"Thank you for your feedback! Average rating: {avg:.1f}")
        except (TypeError, ValueError) as e:
            print(f"Invalid feedback: {e}")
