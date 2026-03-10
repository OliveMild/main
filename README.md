# main

A simple Python application with a user feedback feature.

## Usage

### Greet someone

```bash
python hello.py          # prints "Hello World"
python hello.py Alice    # prints "Hello Alice"
```

### Manage feedback

```python
from feedback import submit_feedback, get_feedback, get_average_rating

# Submit feedback (rating must be 1–5)
submit_feedback("Alice", "Great app!", 5)

# Retrieve all feedback entries
entries = get_feedback()

# Get the average rating
avg = get_average_rating()
```

## Running tests

```bash
python -m unittest discover
```
