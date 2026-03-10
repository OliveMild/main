# main

## User Feedback Feature

`user_feedback.py` provides an in-memory system for collecting and querying user feedback.

### Core API

- **`FeedbackStore.submit(name, email, rating, comment="") → Feedback`** — validates inputs and stores a new feedback entry
- **`FeedbackStore.get(feedback_id) → Feedback`** — retrieve a single entry by ID
- **`FeedbackStore.all() → list[Feedback]`** — return all entries in submission order
- **`FeedbackStore.filter_by_rating(rating) → list[Feedback]`** — return entries matching the given rating
- **`FeedbackStore.average_rating() → float | None`** — mean rating across all entries, or `None` if empty
- **`Feedback.to_dict() → dict`** — serialize a feedback entry to a plain dictionary
- **`ValidationError`** / **`FeedbackNotFoundError`** — typed exceptions for bad input and missing entries

### Validation rules

| Field | Constraints |
|---|---|
| `name` | 1–100 chars, stripped of leading/trailing whitespace |
| `email` | must contain `@` and a domain with a `.` |
| `rating` | integer 1–5 (inclusive); booleans and floats are rejected |
| `comment` | string, max 1000 chars (optional, defaults to `""`) |

### Quick start

```python
from user_feedback import FeedbackStore

store = FeedbackStore()
fb = store.submit("Alice", "alice@example.com", 5, "Absolutely love it!")
print(fb.feedback_id)          # 1
print(store.average_rating())  # 5.0
```

### Running tests

```bash
python -m pytest test_user_feedback.py -v
```