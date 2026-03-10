#!/usr/bin/env python3
"""Tests for the user_feedback module."""

import pytest
from user_feedback import (
    Feedback,
    FeedbackNotFoundError,
    FeedbackStore,
    ValidationError,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_store(*args, **kwargs) -> FeedbackStore:
    """Return a fresh FeedbackStore, optionally pre-populated."""
    store = FeedbackStore()
    if args or kwargs:
        store.submit(*args, **kwargs)
    return store


# ---------------------------------------------------------------------------
# submit – happy path
# ---------------------------------------------------------------------------


class TestSubmitHappyPath:
    def test_returns_feedback_object(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5, "Great!")
        assert isinstance(fb, Feedback)

    def test_auto_increments_id(self):
        store = FeedbackStore()
        fb1 = store.submit("Alice", "alice@example.com", 5)
        fb2 = store.submit("Bob", "bob@example.com", 3)
        assert fb1.feedback_id == 1
        assert fb2.feedback_id == 2

    def test_stores_fields_correctly(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 4, "Nice app")
        assert fb.name == "Alice"
        assert fb.email == "alice@example.com"
        assert fb.rating == 4
        assert fb.comment == "Nice app"

    def test_name_is_stripped(self):
        store = FeedbackStore()
        fb = store.submit("  Alice  ", "alice@example.com", 3)
        assert fb.name == "Alice"

    def test_comment_defaults_to_empty_string(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5)
        assert fb.comment == ""

    def test_created_at_is_set(self):
        from datetime import datetime, timezone

        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5)
        assert isinstance(fb.created_at, datetime)
        assert fb.created_at.tzinfo is not None

    def test_rating_boundaries(self):
        store = FeedbackStore()
        fb1 = store.submit("A", "a@b.com", 1)
        fb5 = store.submit("B", "b@c.com", 5)
        assert fb1.rating == 1
        assert fb5.rating == 5


# ---------------------------------------------------------------------------
# submit – validation errors
# ---------------------------------------------------------------------------


class TestSubmitValidation:
    # name
    def test_empty_name_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("", "a@b.com", 3)

    def test_whitespace_only_name_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("   ", "a@b.com", 3)

    def test_name_too_long_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("x" * 101, "a@b.com", 3)

    def test_name_100_chars_is_ok(self):
        store = FeedbackStore()
        fb = store.submit("x" * 100, "a@b.com", 3)
        assert len(fb.name) == 100

    def test_non_string_name_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit(123, "a@b.com", 3)

    # email
    def test_missing_at_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "notanemail", 3)

    def test_missing_domain_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "alice@", 3)

    def test_whitespace_in_email_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "al ice@ex.com", 3)

    def test_non_string_email_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", None, 3)

    # rating
    def test_rating_zero_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", 0)

    def test_rating_six_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", 6)

    def test_negative_rating_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", -1)

    def test_float_rating_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", 3.0)

    def test_bool_rating_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", True)

    def test_string_rating_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", "5")

    # comment
    def test_comment_too_long_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", 3, "x" * 1001)

    def test_comment_1000_chars_is_ok(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "a@b.com", 3, "x" * 1000)
        assert len(fb.comment) == 1000

    def test_non_string_comment_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.submit("Alice", "a@b.com", 3, 42)


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing_entry(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5, "Love it")
        retrieved = store.get(fb.feedback_id)
        assert retrieved is fb

    def test_get_missing_raises(self):
        store = FeedbackStore()
        with pytest.raises(FeedbackNotFoundError):
            store.get(999)

    def test_get_after_multiple_submissions(self):
        store = FeedbackStore()
        store.submit("A", "a@x.com", 1)
        fb2 = store.submit("B", "b@x.com", 2)
        store.submit("C", "c@x.com", 3)
        assert store.get(2) is fb2


# ---------------------------------------------------------------------------
# all
# ---------------------------------------------------------------------------


class TestAll:
    def test_all_empty(self):
        store = FeedbackStore()
        assert store.all() == []

    def test_all_returns_copy(self):
        store = FeedbackStore()
        store.submit("Alice", "alice@example.com", 4)
        result = store.all()
        result.clear()
        assert len(store) == 1

    def test_all_returns_in_order(self):
        store = FeedbackStore()
        fb1 = store.submit("A", "a@x.com", 1)
        fb2 = store.submit("B", "b@x.com", 2)
        fb3 = store.submit("C", "c@x.com", 3)
        assert store.all() == [fb1, fb2, fb3]


# ---------------------------------------------------------------------------
# filter_by_rating
# ---------------------------------------------------------------------------


class TestFilterByRating:
    def test_filter_returns_matching(self):
        store = FeedbackStore()
        fb1 = store.submit("A", "a@x.com", 5)
        store.submit("B", "b@x.com", 3)
        fb3 = store.submit("C", "c@x.com", 5)
        result = store.filter_by_rating(5)
        assert result == [fb1, fb3]

    def test_filter_returns_empty_when_none_match(self):
        store = FeedbackStore()
        store.submit("A", "a@x.com", 4)
        assert store.filter_by_rating(2) == []

    def test_filter_invalid_rating_raises(self):
        store = FeedbackStore()
        with pytest.raises(ValidationError):
            store.filter_by_rating(6)


# ---------------------------------------------------------------------------
# average_rating
# ---------------------------------------------------------------------------


class TestAverageRating:
    def test_empty_store_returns_none(self):
        store = FeedbackStore()
        assert store.average_rating() is None

    def test_single_entry(self):
        store = FeedbackStore()
        store.submit("Alice", "alice@example.com", 4)
        assert store.average_rating() == 4.0

    def test_multiple_entries(self):
        store = FeedbackStore()
        store.submit("A", "a@x.com", 2)
        store.submit("B", "b@x.com", 4)
        assert store.average_rating() == 3.0

    def test_non_integer_average(self):
        store = FeedbackStore()
        store.submit("A", "a@x.com", 1)
        store.submit("B", "b@x.com", 2)
        avg = store.average_rating()
        assert abs(avg - 1.5) < 1e-9


# ---------------------------------------------------------------------------
# __len__
# ---------------------------------------------------------------------------


class TestLen:
    def test_empty(self):
        store = FeedbackStore()
        assert len(store) == 0

    def test_after_submissions(self):
        store = FeedbackStore()
        store.submit("A", "a@x.com", 1)
        store.submit("B", "b@x.com", 2)
        assert len(store) == 2


# ---------------------------------------------------------------------------
# Feedback.to_dict
# ---------------------------------------------------------------------------


class TestFeedbackToDict:
    def test_to_dict_keys(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5, "Excellent")
        d = fb.to_dict()
        assert set(d.keys()) == {
            "feedback_id",
            "name",
            "email",
            "rating",
            "comment",
            "created_at",
        }

    def test_to_dict_values(self):
        store = FeedbackStore()
        fb = store.submit("Alice", "alice@example.com", 5, "Excellent")
        d = fb.to_dict()
        assert d["feedback_id"] == 1
        assert d["name"] == "Alice"
        assert d["email"] == "alice@example.com"
        assert d["rating"] == 5
        assert d["comment"] == "Excellent"
        assert isinstance(d["created_at"], str)
