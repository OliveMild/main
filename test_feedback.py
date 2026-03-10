#!/usr/bin/env python3
"""Tests for the feedback module."""

import pytest

from feedback import Feedback, FeedbackManager, ValidationError


# ---------------------------------------------------------------------------
# Feedback.__init__ – validation
# ---------------------------------------------------------------------------


class TestFeedbackInit:
    def test_valid_feedback_created(self):
        f = Feedback("alice", "Great product!", 5)
        assert f.user_id == "alice"
        assert f.message == "Great product!"
        assert f.rating == 5

    def test_id_is_set(self):
        f = Feedback("alice", "Good", 4)
        assert f.id is not None
        assert len(f.id) > 0

    def test_unique_ids(self):
        f1 = Feedback("alice", "Good", 4)
        f2 = Feedback("alice", "Good", 4)
        assert f1.id != f2.id

    def test_created_at_is_set(self):
        f = Feedback("alice", "Good", 4)
        assert f.created_at is not None

    # --- user_id validation ---

    def test_empty_user_id_raises(self):
        with pytest.raises(ValidationError):
            Feedback("", "message", 3)

    def test_whitespace_only_user_id_raises(self):
        with pytest.raises(ValidationError):
            Feedback("   ", "message", 3)

    def test_user_id_with_space_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice bob", "message", 3)

    def test_too_long_user_id_raises(self):
        with pytest.raises(ValidationError):
            Feedback("a" * 51, "message", 3)

    def test_max_length_user_id_passes(self):
        f = Feedback("a" * 50, "message", 3)
        assert len(f.user_id) == 50

    def test_non_string_user_id_raises(self):
        with pytest.raises(ValidationError):
            Feedback(123, "message", 3)  # type: ignore[arg-type]

    # --- message validation ---

    def test_empty_message_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "", 3)

    def test_whitespace_only_message_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "   ", 3)

    def test_too_long_message_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "x" * 1001, 3)

    def test_max_length_message_passes(self):
        f = Feedback("alice", "x" * 1000, 3)
        assert len(f.message) == 1000

    def test_non_string_message_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", None, 3)  # type: ignore[arg-type]

    # --- rating validation ---

    def test_rating_1_passes(self):
        f = Feedback("alice", "Terrible", 1)
        assert f.rating == 1

    def test_rating_5_passes(self):
        f = Feedback("alice", "Excellent", 5)
        assert f.rating == 5

    def test_rating_0_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", 0)

    def test_rating_6_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", 6)

    def test_negative_rating_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", -1)

    def test_float_rating_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", 3.5)  # type: ignore[arg-type]

    def test_bool_rating_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", True)  # type: ignore[arg-type]

    def test_non_numeric_rating_raises(self):
        with pytest.raises(ValidationError):
            Feedback("alice", "message", "5")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# FeedbackManager.submit
# ---------------------------------------------------------------------------


class TestFeedbackManagerSubmit:
    def setup_method(self):
        self.manager = FeedbackManager()

    def test_submit_returns_feedback(self):
        fb = self.manager.submit("alice", "Great!", 5)
        assert isinstance(fb, Feedback)

    def test_submit_stores_entry(self):
        fb = self.manager.submit("alice", "Great!", 5)
        assert len(self.manager) == 1
        assert self.manager.get(fb.id) is fb

    def test_multiple_submissions_increment_count(self):
        self.manager.submit("alice", "Good", 4)
        self.manager.submit("bob", "Bad", 2)
        assert len(self.manager) == 2

    def test_submit_with_invalid_user_id_raises(self):
        with pytest.raises(ValidationError):
            self.manager.submit("", "message", 3)

    def test_submit_with_invalid_message_raises(self):
        with pytest.raises(ValidationError):
            self.manager.submit("alice", "", 3)

    def test_submit_with_invalid_rating_raises(self):
        with pytest.raises(ValidationError):
            self.manager.submit("alice", "message", 6)

    def test_submit_does_not_store_on_validation_error(self):
        try:
            self.manager.submit("alice", "", 3)
        except ValidationError:
            pass
        assert len(self.manager) == 0


# ---------------------------------------------------------------------------
# FeedbackManager.get
# ---------------------------------------------------------------------------


class TestFeedbackManagerGet:
    def setup_method(self):
        self.manager = FeedbackManager()

    def test_get_existing_returns_feedback(self):
        fb = self.manager.submit("alice", "Great!", 5)
        assert self.manager.get(fb.id) is fb

    def test_get_nonexistent_returns_none(self):
        assert self.manager.get("nonexistent-id") is None


# ---------------------------------------------------------------------------
# FeedbackManager.list_all
# ---------------------------------------------------------------------------


class TestFeedbackManagerListAll:
    def setup_method(self):
        self.manager = FeedbackManager()

    def test_empty_manager_returns_empty_list(self):
        assert self.manager.list_all() == []

    def test_list_all_returns_all_entries(self):
        fb1 = self.manager.submit("alice", "Good", 4)
        fb2 = self.manager.submit("bob", "Bad", 2)
        result = self.manager.list_all()
        assert len(result) == 2
        assert fb1 in result
        assert fb2 in result

    def test_list_all_ordered_by_created_at(self):
        fb1 = self.manager.submit("alice", "First", 3)
        fb2 = self.manager.submit("bob", "Second", 4)
        result = self.manager.list_all()
        assert result[0].created_at <= result[1].created_at
        assert result[0] is fb1
        assert result[1] is fb2


# ---------------------------------------------------------------------------
# FeedbackManager.get_by_user
# ---------------------------------------------------------------------------


class TestFeedbackManagerGetByUser:
    def setup_method(self):
        self.manager = FeedbackManager()

    def test_get_by_user_returns_only_that_users_entries(self):
        fb1 = self.manager.submit("alice", "First", 4)
        self.manager.submit("bob", "Other", 3)
        fb2 = self.manager.submit("alice", "Second", 5)
        result = self.manager.get_by_user("alice")
        assert len(result) == 2
        assert fb1 in result
        assert fb2 in result

    def test_get_by_user_excludes_other_users(self):
        self.manager.submit("bob", "Other", 3)
        result = self.manager.get_by_user("alice")
        assert result == []

    def test_get_by_user_ordered_by_created_at(self):
        fb1 = self.manager.submit("alice", "First", 3)
        fb2 = self.manager.submit("alice", "Second", 4)
        result = self.manager.get_by_user("alice")
        assert result[0] is fb1
        assert result[1] is fb2

    def test_get_by_unknown_user_returns_empty_list(self):
        assert self.manager.get_by_user("nobody") == []


# ---------------------------------------------------------------------------
# FeedbackManager.delete
# ---------------------------------------------------------------------------


class TestFeedbackManagerDelete:
    def setup_method(self):
        self.manager = FeedbackManager()

    def test_delete_existing_returns_true(self):
        fb = self.manager.submit("alice", "Great!", 5)
        assert self.manager.delete(fb.id) is True

    def test_delete_removes_entry(self):
        fb = self.manager.submit("alice", "Great!", 5)
        self.manager.delete(fb.id)
        assert len(self.manager) == 0
        assert self.manager.get(fb.id) is None

    def test_delete_nonexistent_returns_false(self):
        assert self.manager.delete("nonexistent-id") is False

    def test_delete_does_not_affect_other_entries(self):
        fb1 = self.manager.submit("alice", "First", 4)
        fb2 = self.manager.submit("bob", "Second", 3)
        self.manager.delete(fb1.id)
        assert self.manager.get(fb2.id) is fb2
        assert len(self.manager) == 1
