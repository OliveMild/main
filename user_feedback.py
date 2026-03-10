#!/usr/bin/env python3
"""User feedback module: submission, validation, and retrieval."""

import re
from datetime import datetime, timezone


class UserFeedbackError(Exception):
    """Base exception for user feedback errors."""


class InvalidRatingError(UserFeedbackError):
    """Raised when a feedback rating is invalid."""


class InvalidCommentError(UserFeedbackError):
    """Raised when a feedback comment is invalid."""


class InvalidUserIdError(UserFeedbackError):
    """Raised when a user ID is invalid."""


class FeedbackNotFoundError(UserFeedbackError):
    """Raised when a requested feedback item does not exist."""


_USER_ID_RE = re.compile(r'^[A-Za-z0-9_]{1,64}$')

RATING_MIN = 1
RATING_MAX = 5
COMMENT_MAX_LENGTH = 1000


def _validate_user_id(user_id):
    if not isinstance(user_id, str) or not _USER_ID_RE.match(user_id):
        raise InvalidUserIdError(
            "user_id must be a non-empty string of up to 64 alphanumeric "
            "characters or underscores."
        )


def _validate_rating(rating):
    if not isinstance(rating, int) or isinstance(rating, bool):
        raise InvalidRatingError(
            f"rating must be an integer between {RATING_MIN} and {RATING_MAX}."
        )
    if not (RATING_MIN <= rating <= RATING_MAX):
        raise InvalidRatingError(
            f"rating must be between {RATING_MIN} and {RATING_MAX}, got {rating}."
        )


def _validate_comment(comment):
    if not isinstance(comment, str):
        raise InvalidCommentError("comment must be a string.")
    if len(comment) > COMMENT_MAX_LENGTH:
        raise InvalidCommentError(
            f"comment must not exceed {COMMENT_MAX_LENGTH} characters."
        )


class UserFeedback:
    """Represents a single piece of user feedback."""

    def __init__(self, user_id, rating, comment=""):
        _validate_user_id(user_id)
        _validate_rating(rating)
        _validate_comment(comment)
        self._user_id = user_id
        self._rating = rating
        self._comment = comment
        self._created_at = datetime.now(timezone.utc)

    @property
    def user_id(self):
        return self._user_id

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        _validate_rating(value)
        self._rating = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        _validate_comment(value)
        self._comment = value

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self):
        """Return a plain-dict serialisation of this feedback item."""
        return {
            "user_id": self._user_id,
            "rating": self._rating,
            "comment": self._comment,
            "created_at": self._created_at.isoformat(),
        }

    def __repr__(self):
        return (
            f"UserFeedback(user_id={self._user_id!r}, "
            f"rating={self._rating}, comment={self._comment!r})"
        )


class FeedbackStore:
    """In-memory store for UserFeedback items."""

    def __init__(self):
        self._items = []

    def submit(self, user_id, rating, comment=""):
        """Create and store a new feedback item; returns the item."""
        feedback = UserFeedback(user_id=user_id, rating=rating, comment=comment)
        self._items.append(feedback)
        return feedback

    def get_all(self):
        """Return a copy of all stored feedback items."""
        return list(self._items)

    def get_by_user(self, user_id):
        """Return all feedback submitted by *user_id*."""
        _validate_user_id(user_id)
        return [item for item in self._items if item.user_id == user_id]

    def average_rating(self):
        """Return the average rating across all stored feedback, or None if empty."""
        if not self._items:
            return None
        return sum(item.rating for item in self._items) / len(self._items)

    def __len__(self):
        return len(self._items)
