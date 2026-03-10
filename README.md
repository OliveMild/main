# main

A simple Python application that greets the user and collects feedback.

## Usage

```bash
python3 hello.py
```

The application will print "Hello World" and then prompt you to submit feedback.

## Feedback Module

You can also use the feedback module directly:

```python
from feedback import submit_feedback, get_all_feedback

# Submit feedback
submit_feedback("Alice", "Great app!")

# Retrieve all feedback
entries = get_all_feedback()
```

Feedback is persisted to `feedback.json` in the current directory.

## Running Tests

```bash
python3 -m unittest test_feedback -v
```