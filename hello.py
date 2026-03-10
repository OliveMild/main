#!/usr/bin/env python3


class FeedbackCollector:
    """Collects and displays user feedback."""

    def __init__(self):
        self.feedback_list = []

    def collect_feedback(self):
        """Prompt the user to enter feedback and store it."""
        feedback = input("Please enter your feedback: ").strip()
        if feedback:
            self.feedback_list.append(feedback)
            print("Thank you for your feedback!")
        else:
            print("No feedback provided.")

    def view_feedback(self):
        """Display all collected feedback."""
        if not self.feedback_list:
            print("No feedback collected yet.")
        else:
            print("Collected feedback:")
            for i, feedback_item in enumerate(self.feedback_list, start=1):
                print(f"  {i}. {feedback_item}")


if __name__ == "__main__":
    print("Hello World")
    collector = FeedbackCollector()
    collector.collect_feedback()
    collector.view_feedback()
