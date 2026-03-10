#!/usr/bin/env python3
"""Tests for the user feedback module."""

import pytest

from feedback import (
    Feedback,
    FeedbackStore,
    ValidationError,
    _validate_message,
    _validate_rating,
    _validate_username,
)


# ---------------------------------------------------------------------------
# Feedback dataclass
# ---------------------------------------------------------------------------

class TestFeedback:
    def test_feedback_attributes(self):
        fb = Feedback("alice", "Great app!", 5)
        assert fb.username == "alice"
        assert fb.message == "Great app!"
        assert fb.rating == 5

    def test_feedback_has_created_at(self):
        fb = Feedback("alice", "Great app!", 5)
        assert fb.created_at is not None

    def test_feedback_repr(self):
        fb = Feedback("alice", "Great app!", 5)
        r = repr(fb)
        assert "alice" in r
        assert "5" in r


# ---------------------------------------------------------------------------
# _validate_username
# ---------------------------------------------------------------------------

class TestValidateUsername:
    def test_empty_username_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("")

    def test_whitespace_username_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("   ")

    def test_too_long_username_raises(self):
        with pytest.raises(ValidationError):
            _validate_username("a" * 51)

    def test_special_chars_raise(self):
        with pytest.raises(ValidationError):
            _validate_username("ali ce")

    def test_valid_alphanumeric_username(self):
        _validate_username("alice123")  # should not raise

    def test_valid_username_with_underscore(self):
        _validate_username("alice_99")  # should not raise


# ---------------------------------------------------------------------------
# _validate_message
# ---------------------------------------------------------------------------

class TestValidateMessage:
    def test_empty_message_raises(self):
        with pytest.raises(ValidationError):
            _validate_message("")

    def test_whitespace_only_message_raises(self):
        with pytest.raises(ValidationError):
            _validate_message("   ")

    def test_too_long_message_raises(self):
        with pytest.raises(ValidationError):
            _validate_message("x" * 1001)

    def test_valid_message(self):
        _validate_message("This is great!")  # should not raise

    def test_max_length_message_is_valid(self):
        _validate_message("x" * 1000)  # should not raise


# ---------------------------------------------------------------------------
# _validate_rating
# ---------------------------------------------------------------------------

class TestValidateRating:
    def test_rating_below_min_raises(self):
        with pytest.raises(ValidationError):
            _validate_rating(0)

    def test_rating_above_max_raises(self):
        with pytest.raises(ValidationError):
            _validate_rating(6)

    def test_non_integer_rating_raises(self):
        with pytest.raises(ValidationError):
            _validate_rating(3.5)  # type: ignore[arg-type]

    def test_valid_rating_1(self):
        _validate_rating(1)  # should not raise

    def test_valid_rating_5(self):
        _validate_rating(5)  # should not raise

    def test_valid_rating_3(self):
        _validate_rating(3)  # should not raise


# ---------------------------------------------------------------------------
# FeedbackStore.submit – happy path
# ---------------------------------------------------------------------------

class TestFeedbackStoreSubmit:
    def setup_method(self):
        self.store = FeedbackStore()

    def test_submit_returns_feedback(self):
        fb = self.store.submit("alice", "Great!", 5)
        assert isinstance(fb, Feedback)

    def test_submitted_feedback_attributes(self):
        fb = self.store.submit("alice", "Needs work.", 3)
        assert fb.username == "alice"
        assert fb.message == "Needs work."
        assert fb.rating == 3

    def test_store_length_increases(self):
        assert len(self.store) == 0
        self.store.submit("alice", "Good.", 4)
        assert len(self.store) == 1
        self.store.submit("bob", "Bad.", 2)
        assert len(self.store) == 2

    def test_same_user_can_submit_multiple_times(self):
        self.store.submit("alice", "First thought.", 4)
        self.store.submit("alice", "Changed my mind.", 5)
        assert len(self.store) == 2


# ---------------------------------------------------------------------------
# FeedbackStore.submit – validation errors
# ---------------------------------------------------------------------------

class TestFeedbackStoreSubmitValidation:
    def setup_method(self):
        self.store = FeedbackStore()

    def test_invalid_username_raises(self):
        with pytest.raises(ValidationError):
            self.store.submit("", "Good app.", 5)

    def test_invalid_message_raises(self):
        with pytest.raises(ValidationError):
            self.store.submit("alice", "", 5)

    def test_invalid_rating_raises(self):
        with pytest.raises(ValidationError):
            self.store.submit("alice", "Good app.", 0)

    def test_store_unchanged_after_validation_error(self):
        try:
            self.store.submit("", "Good app.", 5)
        except ValidationError:
            pass
        assert len(self.store) == 0


# ---------------------------------------------------------------------------
# FeedbackStore.get_all
# ---------------------------------------------------------------------------

class TestFeedbackStoreGetAll:
    def setup_method(self):
        self.store = FeedbackStore()

    def test_get_all_empty(self):
        assert self.store.get_all() == []

    def test_get_all_returns_all_entries(self):
        self.store.submit("alice", "Good.", 4)
        self.store.submit("bob", "Bad.", 2)
        entries = self.store.get_all()
        assert len(entries) == 2

    def test_get_all_returns_copy(self):
        self.store.submit("alice", "Good.", 4)
        entries = self.store.get_all()
        entries.clear()
        assert len(self.store) == 1


# ---------------------------------------------------------------------------
# FeedbackStore.get_by_user
# ---------------------------------------------------------------------------

class TestFeedbackStoreGetByUser:
    def setup_method(self):
        self.store = FeedbackStore()
        self.store.submit("alice", "First.", 5)
        self.store.submit("bob", "My view.", 3)
        self.store.submit("alice", "Second.", 4)

    def test_get_by_user_returns_only_that_user(self):
        entries = self.store.get_by_user("alice")
        assert len(entries) == 2
        assert all(e.username == "alice" for e in entries)

    def test_get_by_user_case_insensitive(self):
        entries = self.store.get_by_user("ALICE")
        assert len(entries) == 2

    def test_get_by_unknown_user_returns_empty(self):
        entries = self.store.get_by_user("charlie")
        assert entries == []


# ---------------------------------------------------------------------------
# FeedbackStore.average_rating
# ---------------------------------------------------------------------------

class TestFeedbackStoreAverageRating:
    def setup_method(self):
        self.store = FeedbackStore()

    def test_average_rating_empty_store(self):
        assert self.store.average_rating() == 0.0

    def test_average_rating_single_entry(self):
        self.store.submit("alice", "Good.", 4)
        assert self.store.average_rating() == 4.0

    def test_average_rating_multiple_entries(self):
        self.store.submit("alice", "Good.", 4)
        self.store.submit("bob", "Bad.", 2)
        assert self.store.average_rating() == 3.0

    def test_average_rating_all_same(self):
        for i in range(5):
            self.store.submit(f"user{i}", "Feedback.", 5)
        assert self.store.average_rating() == 5.0
