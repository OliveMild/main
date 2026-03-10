#!/usr/bin/env python3

from feedback import submit_feedback, get_average_rating

if __name__ == "__main__":
    print("Hello World")
    try:
        rating = int(input("Please rate your experience (1-5): "))
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        comment = input("Any comments? (press Enter to skip): ")
        submit_feedback(rating, comment)
        avg = get_average_rating()
        print(f"Thank you for your feedback! Average rating: {avg:.1f}")
