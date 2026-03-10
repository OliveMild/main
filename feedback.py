#!/usr/bin/env python3
"""User feedback module."""

import re
from datetime import datetime


class ValidationError(Exception):
    """Raised when feedback input fails validation."""


_MESSAGE_MAX_LENGTH = 1000
_USERNAME_MAX_LENGTH = 50
_RATING_MIN = 1
_RATING_MAX = 5


def _validate_username(username: str) -> None:
    if not username or not username.strip():
        raise ValidationError("Username must not be empty.")
    if len(username) > _USERNAME_MAX_LENGTH:
        raise ValidationError(
            f"Username must not exceed {_USERNAME_MAX_LENGTH} characters."
        )
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        raise ValidationError(
            "Username may only contain letters, digits, and underscores."
        )


def _validate_message(message: str) -> None:
    if not message or not message.strip():
        raise ValidationError("Feedback message must not be empty.")
    if len(message) > _MESSAGE_MAX_LENGTH:
        raise ValidationError(
            f"Feedback message must not exceed {_MESSAGE_MAX_LENGTH} characters."
        )


def _validate_rating(rating: int) -> None:
    if not isinstance(rating, int):
        raise ValidationError("Rating must be an integer.")
    if rating < _RATING_MIN or rating > _RATING_MAX:
        raise ValidationError(
            f"Rating must be between {_RATING_MIN} and {_RATING_MAX}."
        )


class Feedback:
    """Represents a piece of user feedback."""

    def __init__(self, username: str, message: str, rating: int) -> None:
        self.username = username
        self.message = message
        self.rating = rating
        self.created_at: datetime = datetime.now()

    def __repr__(self) -> str:
        return (
            f"Feedback(username={self.username!r}, rating={self.rating}, "
            f"message={self.message!r})"
        )


class FeedbackStore:
    """Manages a collection of user feedback entries."""

    def __init__(self) -> None:
        self._entries: list[Feedback] = []

    def submit(self, username: str, message: str, rating: int) -> Feedback:
        """Validate and store a feedback entry, then return the Feedback object.

        Args:
            username: The name of the user submitting feedback.
            message: The feedback text.
            rating: A star rating between 1 and 5 (inclusive).

        Raises:
            ValidationError: If any input fails validation.
        """
        _validate_username(username)
        _validate_message(message)
        _validate_rating(rating)

        entry = Feedback(username, message, rating)
        self._entries.append(entry)
        return entry

    def get_all(self) -> list[Feedback]:
        """Return all feedback entries in submission order."""
        return list(self._entries)

    def get_by_user(self, username: str) -> list[Feedback]:
        """Return all feedback entries submitted by the given username (case-insensitive)."""
        lower = username.lower()
        return [e for e in self._entries if e.username.lower() == lower]

    def average_rating(self) -> float:
        """Return the average rating across all feedback entries.

        Returns 0.0 if there are no entries.
        """
        if not self._entries:
            return 0.0
        return sum(e.rating for e in self._entries) / len(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
