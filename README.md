# main

## Task Manager Feature

`task_manager.py` provides an in-memory system for creating and tracking tasks.

### Core API

- **`TaskStore.create(title, description="") → Task`** — validates inputs and creates a new task (status defaults to `OPEN`)
- **`TaskStore.get(task_id) → Task`** — retrieve a single task by ID
- **`TaskStore.all() → list[Task]`** — return all tasks in creation order
- **`TaskStore.update(task_id, title=None, description=None, status=None) → Task`** — update one or more fields of an existing task
- **`TaskStore.delete(task_id) → None`** — remove a task by ID
- **`TaskStore.filter_by_status(status) → list[Task]`** — return tasks matching the given status
- **`Task.to_dict() → dict`** — serialize a task to a plain dictionary
- **`Status`** — enum with values `OPEN`, `IN_PROGRESS`, `DONE`
- **`ValidationError`** / **`TaskNotFoundError`** — typed exceptions for bad input and missing tasks

### Validation rules

| Field | Constraints |
|---|---|
| `title` | 1–200 chars, stripped of leading/trailing whitespace |
| `description` | string, max 2000 chars (optional, defaults to `""`) |
| `status` | must be a `Status` enum value |

### Quick start

```python
from task_manager import TaskStore, Status

store = TaskStore()
task = store.create("Fix login bug", "Users cannot log in with email addresses")
print(task.task_id)      # 1
print(task.status)       # Status.OPEN

store.update(task.task_id, status=Status.IN_PROGRESS)
print(task.status)       # Status.IN_PROGRESS

done_tasks = store.filter_by_status(Status.DONE)
```

### Running tests

```bash
python -m pytest test_task_manager.py -v
```