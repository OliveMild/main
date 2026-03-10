#!/usr/bin/env python3
"""Tests for the task_manager module."""

import pytest
from task_manager import (
    Status,
    Task,
    TaskNotFoundError,
    TaskStore,
    ValidationError,
)


# ---------------------------------------------------------------------------
# create – happy path
# ---------------------------------------------------------------------------


class TestCreateHappyPath:
    def test_returns_task_object(self):
        store = TaskStore()
        task = store.create("Buy groceries")
        assert isinstance(task, Task)

    def test_auto_increments_id(self):
        store = TaskStore()
        t1 = store.create("Task one")
        t2 = store.create("Task two")
        assert t1.task_id == 1
        assert t2.task_id == 2

    def test_stores_fields_correctly(self):
        store = TaskStore()
        task = store.create("Fix bug", "Investigate the login issue")
        assert task.title == "Fix bug"
        assert task.description == "Investigate the login issue"
        assert task.status == Status.OPEN

    def test_title_is_stripped(self):
        store = TaskStore()
        task = store.create("  Write tests  ")
        assert task.title == "Write tests"

    def test_description_defaults_to_empty_string(self):
        store = TaskStore()
        task = store.create("Stand-up")
        assert task.description == ""

    def test_default_status_is_open(self):
        store = TaskStore()
        task = store.create("Initial task")
        assert task.status == Status.OPEN

    def test_created_at_is_set(self):
        from datetime import datetime, timezone

        store = TaskStore()
        task = store.create("Timestamp check")
        assert isinstance(task.created_at, datetime)
        assert task.created_at.tzinfo is not None

    def test_title_at_max_length(self):
        store = TaskStore()
        task = store.create("x" * 200)
        assert len(task.title) == 200

    def test_description_at_max_length(self):
        store = TaskStore()
        task = store.create("Long desc", "y" * 2000)
        assert len(task.description) == 2000


# ---------------------------------------------------------------------------
# create – validation errors
# ---------------------------------------------------------------------------


class TestCreateValidation:
    # title
    def test_empty_title_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create("")

    def test_whitespace_only_title_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create("   ")

    def test_title_too_long_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create("x" * 201)

    def test_non_string_title_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create(123)

    def test_none_title_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create(None)

    # description
    def test_description_too_long_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create("Valid title", "x" * 2001)

    def test_non_string_description_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.create("Valid title", 42)


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing_task(self):
        store = TaskStore()
        task = store.create("Deploy app")
        retrieved = store.get(task.task_id)
        assert retrieved is task

    def test_get_missing_raises(self):
        store = TaskStore()
        with pytest.raises(TaskNotFoundError):
            store.get(999)

    def test_get_after_multiple_creations(self):
        store = TaskStore()
        store.create("A")
        t2 = store.create("B")
        store.create("C")
        assert store.get(2) is t2


# ---------------------------------------------------------------------------
# all
# ---------------------------------------------------------------------------


class TestAll:
    def test_all_empty(self):
        store = TaskStore()
        assert store.all() == []

    def test_all_returns_copy(self):
        store = TaskStore()
        store.create("Only task")
        result = store.all()
        result.clear()
        assert len(store) == 1

    def test_all_returns_in_order(self):
        store = TaskStore()
        t1 = store.create("First")
        t2 = store.create("Second")
        t3 = store.create("Third")
        assert store.all() == [t1, t2, t3]


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


class TestUpdate:
    def test_update_title(self):
        store = TaskStore()
        task = store.create("Old title")
        updated = store.update(task.task_id, title="New title")
        assert updated.title == "New title"

    def test_update_title_is_stripped(self):
        store = TaskStore()
        task = store.create("Draft")
        store.update(task.task_id, title="  Clean title  ")
        assert task.title == "Clean title"

    def test_update_description(self):
        store = TaskStore()
        task = store.create("Task")
        store.update(task.task_id, description="More detail")
        assert task.description == "More detail"

    def test_update_status(self):
        store = TaskStore()
        task = store.create("Work item")
        store.update(task.task_id, status=Status.IN_PROGRESS)
        assert task.status == Status.IN_PROGRESS

    def test_update_multiple_fields(self):
        store = TaskStore()
        task = store.create("Draft")
        store.update(task.task_id, title="Final", status=Status.DONE)
        assert task.title == "Final"
        assert task.status == Status.DONE

    def test_update_sets_updated_at(self):
        import time

        store = TaskStore()
        task = store.create("Time check")
        original_updated_at = task.updated_at
        time.sleep(0.01)
        store.update(task.task_id, title="Changed")
        assert task.updated_at >= original_updated_at

    def test_update_missing_task_raises(self):
        store = TaskStore()
        with pytest.raises(TaskNotFoundError):
            store.update(999, title="Ghost")

    def test_update_invalid_title_raises(self):
        store = TaskStore()
        task = store.create("Valid")
        with pytest.raises(ValidationError):
            store.update(task.task_id, title="")

    def test_update_invalid_description_raises(self):
        store = TaskStore()
        task = store.create("Valid")
        with pytest.raises(ValidationError):
            store.update(task.task_id, description="x" * 2001)

    def test_update_invalid_status_raises(self):
        store = TaskStore()
        task = store.create("Valid")
        with pytest.raises(ValidationError):
            store.update(task.task_id, status="done")

    def test_update_returns_task(self):
        store = TaskStore()
        task = store.create("Return me")
        result = store.update(task.task_id, title="Returned")
        assert result is task


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_removes_task(self):
        store = TaskStore()
        task = store.create("Temporary")
        store.delete(task.task_id)
        assert len(store) == 0

    def test_delete_missing_raises(self):
        store = TaskStore()
        with pytest.raises(TaskNotFoundError):
            store.delete(999)

    def test_delete_correct_task(self):
        store = TaskStore()
        t1 = store.create("Keep")
        t2 = store.create("Remove")
        store.delete(t2.task_id)
        assert store.all() == [t1]


# ---------------------------------------------------------------------------
# filter_by_status
# ---------------------------------------------------------------------------


class TestFilterByStatus:
    def test_filter_returns_matching(self):
        store = TaskStore()
        t1 = store.create("Open task")
        store.create("Another task")
        store.update(2, status=Status.DONE)
        result = store.filter_by_status(Status.OPEN)
        assert result == [t1]

    def test_filter_returns_empty_when_none_match(self):
        store = TaskStore()
        store.create("Open only")
        assert store.filter_by_status(Status.DONE) == []

    def test_filter_invalid_status_raises(self):
        store = TaskStore()
        with pytest.raises(ValidationError):
            store.filter_by_status("open")

    def test_filter_in_progress(self):
        store = TaskStore()
        store.create("T1")
        t2 = store.create("T2")
        store.update(t2.task_id, status=Status.IN_PROGRESS)
        assert store.filter_by_status(Status.IN_PROGRESS) == [t2]


# ---------------------------------------------------------------------------
# __len__
# ---------------------------------------------------------------------------


class TestLen:
    def test_empty(self):
        store = TaskStore()
        assert len(store) == 0

    def test_after_creations(self):
        store = TaskStore()
        store.create("A")
        store.create("B")
        assert len(store) == 2

    def test_after_deletion(self):
        store = TaskStore()
        task = store.create("Ephemeral")
        store.delete(task.task_id)
        assert len(store) == 0


# ---------------------------------------------------------------------------
# Task.to_dict
# ---------------------------------------------------------------------------


class TestTaskToDict:
    def test_to_dict_keys(self):
        store = TaskStore()
        task = store.create("Review PR", "Check the diff carefully")
        d = task.to_dict()
        assert set(d.keys()) == {
            "task_id",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
        }

    def test_to_dict_values(self):
        store = TaskStore()
        task = store.create("Review PR", "Check the diff carefully")
        d = task.to_dict()
        assert d["task_id"] == 1
        assert d["title"] == "Review PR"
        assert d["description"] == "Check the diff carefully"
        assert d["status"] == "open"
        assert isinstance(d["created_at"], str)
        assert isinstance(d["updated_at"], str)

    def test_to_dict_status_reflects_updates(self):
        store = TaskStore()
        task = store.create("In flight")
        store.update(task.task_id, status=Status.IN_PROGRESS)
        assert task.to_dict()["status"] == "in_progress"


# ---------------------------------------------------------------------------
# Status enum
# ---------------------------------------------------------------------------


class TestStatus:
    def test_all_statuses_available(self):
        assert Status.OPEN.value == "open"
        assert Status.IN_PROGRESS.value == "in_progress"
        assert Status.DONE.value == "done"
