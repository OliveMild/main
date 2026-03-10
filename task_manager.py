#!/usr/bin/env python3
"""Task management module for creating and tracking tasks."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class ValidationError(ValueError):
    """Raised when task input fails validation."""


class TaskNotFoundError(KeyError):
    """Raised when a requested task does not exist."""


class Status(str, Enum):
    """Valid task statuses."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    """Represents a single task."""

    task_id: int
    title: str
    description: str
    status: Status
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """Return a dictionary representation of this task."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


def _validate_title(title: str) -> None:
    if not isinstance(title, str):
        raise ValidationError("title must be a string")
    if not title.strip():
        raise ValidationError("title must be a non-empty string")
    if len(title.strip()) > 200:
        raise ValidationError("title must be 200 characters or fewer")


def _validate_description(description: str) -> None:
    if not isinstance(description, str):
        raise ValidationError("description must be a string")
    if len(description) > 2000:
        raise ValidationError("description must be 2000 characters or fewer")


def _validate_status(status: Status) -> None:
    if not isinstance(status, Status):
        raise ValidationError(
            f"status must be a Status enum value; got {status!r}"
        )


class TaskStore:
    """In-memory store for task entries."""

    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create(self, title: str, description: str = "") -> Task:
        """Validate inputs and create a new task.

        Args:
            title: Short summary of the task (1–200 chars).
            description: Optional detailed description (max 2000 chars).

        Returns:
            The newly created :class:`Task` object.

        Raises:
            ValidationError: If any input fails validation.
        """
        _validate_title(title)
        _validate_description(description)

        now = datetime.now(timezone.utc)
        task = Task(
            task_id=self._next_id,
            title=title.strip(),
            description=description,
            status=Status.OPEN,
            created_at=now,
            updated_at=now,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Return a task by its ID.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        raise TaskNotFoundError(f"no task with id {task_id}")

    def all(self) -> List[Task]:
        """Return all tasks in creation order."""
        return list(self._tasks)

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[Status] = None,
    ) -> Task:
        """Update one or more fields of an existing task.

        Args:
            task_id: ID of the task to update.
            title: New title (optional).
            description: New description (optional).
            status: New status (optional).

        Returns:
            The updated :class:`Task` object.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            ValidationError: If any updated field fails validation.
        """
        task = self.get(task_id)

        if title is not None:
            _validate_title(title)
            task.title = title.strip()

        if description is not None:
            _validate_description(description)
            task.description = description

        if status is not None:
            _validate_status(status)
            task.status = status

        task.updated_at = datetime.now(timezone.utc)
        return task

    def delete(self, task_id: int) -> None:
        """Remove a task by its ID.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                del self._tasks[i]
                return
        raise TaskNotFoundError(f"no task with id {task_id}")

    def filter_by_status(self, status: Status) -> List[Task]:
        """Return all tasks that match the given status.

        Raises:
            ValidationError: If *status* is not a valid :class:`Status` value.
        """
        _validate_status(status)
        return [t for t in self._tasks if t.status == status]

    def __len__(self) -> int:
        return len(self._tasks)
