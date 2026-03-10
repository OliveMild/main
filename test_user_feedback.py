#!/usr/bin/env python3
"""Tests for user_feedback module."""

import unittest

from user_feedback import (
    COMMENT_MAX_LENGTH,
    RATING_MAX,
    RATING_MIN,
    FeedbackNotFoundError,
    FeedbackStore,
    InvalidCommentError,
    InvalidRatingError,
    InvalidUserIdError,
    UserFeedback,
    UserFeedbackError,
)


class TestExceptionHierarchy(unittest.TestCase):
    def test_invalid_rating_is_user_feedback_error(self):
        self.assertTrue(issubclass(InvalidRatingError, UserFeedbackError))

    def test_invalid_comment_is_user_feedback_error(self):
        self.assertTrue(issubclass(InvalidCommentError, UserFeedbackError))

    def test_invalid_user_id_is_user_feedback_error(self):
        self.assertTrue(issubclass(InvalidUserIdError, UserFeedbackError))

    def test_feedback_not_found_is_user_feedback_error(self):
        self.assertTrue(issubclass(FeedbackNotFoundError, UserFeedbackError))


class TestUserFeedbackConstruction(unittest.TestCase):
    def test_valid_construction(self):
        fb = UserFeedback(user_id="alice", rating=4, comment="Great!")
        self.assertEqual(fb.user_id, "alice")
        self.assertEqual(fb.rating, 4)
        self.assertEqual(fb.comment, "Great!")

    def test_default_comment_is_empty_string(self):
        fb = UserFeedback(user_id="bob", rating=3)
        self.assertEqual(fb.comment, "")

    def test_created_at_is_set(self):
        fb = UserFeedback(user_id="carol", rating=5)
        self.assertIsNotNone(fb.created_at)

    def test_minimum_rating(self):
        fb = UserFeedback(user_id="user1", rating=RATING_MIN)
        self.assertEqual(fb.rating, RATING_MIN)

    def test_maximum_rating(self):
        fb = UserFeedback(user_id="user1", rating=RATING_MAX)
        self.assertEqual(fb.rating, RATING_MAX)

    def test_user_id_with_underscores_and_digits(self):
        fb = UserFeedback(user_id="user_123", rating=2)
        self.assertEqual(fb.user_id, "user_123")


class TestUserFeedbackValidationErrors(unittest.TestCase):
    # --- user_id ---
    def test_empty_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            UserFeedback(user_id="", rating=3)

    def test_none_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            UserFeedback(user_id=None, rating=3)

    def test_user_id_with_spaces_raises(self):
        with self.assertRaises(InvalidUserIdError):
            UserFeedback(user_id="bad user", rating=3)

    def test_user_id_too_long_raises(self):
        with self.assertRaises(InvalidUserIdError):
            UserFeedback(user_id="a" * 65, rating=3)

    def test_user_id_exactly_64_chars_is_valid(self):
        fb = UserFeedback(user_id="a" * 64, rating=3)
        self.assertEqual(len(fb.user_id), 64)

    # --- rating ---
    def test_rating_below_min_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating=RATING_MIN - 1)

    def test_rating_above_max_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating=RATING_MAX + 1)

    def test_rating_float_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating=3.0)

    def test_rating_bool_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating=True)

    def test_rating_none_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating=None)

    def test_rating_string_raises(self):
        with self.assertRaises(InvalidRatingError):
            UserFeedback(user_id="alice", rating="5")

    # --- comment ---
    def test_comment_too_long_raises(self):
        with self.assertRaises(InvalidCommentError):
            UserFeedback(user_id="alice", rating=3, comment="x" * (COMMENT_MAX_LENGTH + 1))

    def test_comment_exactly_max_length_is_valid(self):
        fb = UserFeedback(user_id="alice", rating=3, comment="x" * COMMENT_MAX_LENGTH)
        self.assertEqual(len(fb.comment), COMMENT_MAX_LENGTH)

    def test_comment_non_string_raises(self):
        with self.assertRaises(InvalidCommentError):
            UserFeedback(user_id="alice", rating=3, comment=42)


class TestUserFeedbackSetters(unittest.TestCase):
    def setUp(self):
        self.fb = UserFeedback(user_id="alice", rating=3, comment="ok")

    def test_set_valid_rating(self):
        self.fb.rating = 5
        self.assertEqual(self.fb.rating, 5)

    def test_set_invalid_rating_raises(self):
        with self.assertRaises(InvalidRatingError):
            self.fb.rating = 0

    def test_set_valid_comment(self):
        self.fb.comment = "Updated comment"
        self.assertEqual(self.fb.comment, "Updated comment")

    def test_set_invalid_comment_raises(self):
        with self.assertRaises(InvalidCommentError):
            self.fb.comment = "x" * (COMMENT_MAX_LENGTH + 1)


class TestUserFeedbackToDict(unittest.TestCase):
    def test_to_dict_keys(self):
        fb = UserFeedback(user_id="alice", rating=4, comment="Nice")
        d = fb.to_dict()
        self.assertIn("user_id", d)
        self.assertIn("rating", d)
        self.assertIn("comment", d)
        self.assertIn("created_at", d)

    def test_to_dict_values(self):
        fb = UserFeedback(user_id="bob", rating=2, comment="Meh")
        d = fb.to_dict()
        self.assertEqual(d["user_id"], "bob")
        self.assertEqual(d["rating"], 2)
        self.assertEqual(d["comment"], "Meh")


class TestFeedbackStore(unittest.TestCase):
    def setUp(self):
        self.store = FeedbackStore()

    def test_empty_store_len_is_zero(self):
        self.assertEqual(len(self.store), 0)

    def test_submit_returns_feedback(self):
        fb = self.store.submit("alice", 5, "Excellent")
        self.assertIsInstance(fb, UserFeedback)

    def test_submit_increases_len(self):
        self.store.submit("alice", 4)
        self.assertEqual(len(self.store), 1)

    def test_get_all_returns_all_items(self):
        self.store.submit("alice", 4)
        self.store.submit("bob", 2, "Could be better")
        items = self.store.get_all()
        self.assertEqual(len(items), 2)

    def test_get_all_is_copy(self):
        self.store.submit("alice", 4)
        items = self.store.get_all()
        items.clear()
        self.assertEqual(len(self.store), 1)

    def test_get_by_user_filters_correctly(self):
        self.store.submit("alice", 5)
        self.store.submit("bob", 3)
        self.store.submit("alice", 4, "Second feedback")
        alice_items = self.store.get_by_user("alice")
        self.assertEqual(len(alice_items), 2)
        for item in alice_items:
            self.assertEqual(item.user_id, "alice")

    def test_get_by_user_returns_empty_for_unknown_user(self):
        self.store.submit("alice", 5)
        result = self.store.get_by_user("unknown_user")
        self.assertEqual(result, [])

    def test_get_by_user_invalid_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            self.store.get_by_user("")

    def test_average_rating_none_when_empty(self):
        self.assertIsNone(self.store.average_rating())

    def test_average_rating_single_item(self):
        self.store.submit("alice", 4)
        self.assertEqual(self.store.average_rating(), 4.0)

    def test_average_rating_multiple_items(self):
        self.store.submit("alice", 2)
        self.store.submit("bob", 4)
        self.assertAlmostEqual(self.store.average_rating(), 3.0)

    def test_submit_invalid_rating_raises(self):
        with self.assertRaises(InvalidRatingError):
            self.store.submit("alice", 6)

    def test_submit_invalid_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            self.store.submit("", 3)

    def test_submit_invalid_comment_raises(self):
        with self.assertRaises(InvalidCommentError):
            self.store.submit("alice", 3, comment=None)


if __name__ == "__main__":
    unittest.main()
