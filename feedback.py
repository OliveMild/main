#!/usr/bin/env python3
"""User feedback module.

Provides a simple in-memory system for collecting and managing user feedback.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional


class ValidationError(Exception):
    """Raised when a feedback field fails validation."""


_USER_ID_MAX = 50
_MESSAGE_MAX = 1000
_RATING_MIN = 1
_RATING_MAX = 5


def _validate_user_id(user_id: str) -> None:
    if not isinstance(user_id, str) or not user_id or not user_id.strip():
        raise ValidationError("user_id must be a non-empty string.")
    if " " in user_id:
        raise ValidationError("user_id must not contain whitespace.")
    if len(user_id) > _USER_ID_MAX:
        raise ValidationError(f"user_id must not exceed {_USER_ID_MAX} characters.")


def _validate_message(message: str) -> None:
    if not isinstance(message, str) or not message or not message.strip():
        raise ValidationError("Feedback message must be a non-empty string.")
    if len(message) > _MESSAGE_MAX:
        raise ValidationError(
            f"Feedback message must not exceed {_MESSAGE_MAX} characters."
        )


def _validate_rating(rating: int) -> None:
    if not isinstance(rating, int) or isinstance(rating, bool):
        raise ValidationError("Rating must be an integer.")
    if not (_RATING_MIN <= rating <= _RATING_MAX):
        raise ValidationError(
            f"Rating must be between {_RATING_MIN} and {_RATING_MAX} (inclusive)."
        )


class Feedback:
    """Represents a single piece of user feedback."""

    def __init__(self, user_id: str, message: str, rating: int) -> None:
        _validate_user_id(user_id)
        _validate_message(message)
        _validate_rating(rating)
        self.id: str = str(uuid.uuid4())
        self.user_id: str = user_id
        self.message: str = message
        self.rating: int = rating
        self.created_at: datetime = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"Feedback(id={self.id!r}, user_id={self.user_id!r}, "
            f"rating={self.rating!r})"
        )


class FeedbackManager:
    """Manages a collection of user feedback entries."""

    def __init__(self) -> None:
        self._store: dict[str, Feedback] = {}

    def submit(self, user_id: str, message: str, rating: int) -> Feedback:
        """Create and store a new feedback entry.

        Args:
            user_id: Identifier of the user submitting feedback.
            message: The feedback text.
            rating:  A score from 1 (lowest) to 5 (highest).

        Returns:
            The newly created :class:`Feedback` instance.

        Raises:
            ValidationError: If any field fails validation.
        """
        feedback = Feedback(user_id, message, rating)
        self._store[feedback.id] = feedback
        return feedback

    def get(self, feedback_id: str) -> Optional[Feedback]:
        """Return the feedback entry with *feedback_id*, or None if not found."""
        return self._store.get(feedback_id)

    def list_all(self) -> List[Feedback]:
        """Return all feedback entries ordered by creation time (oldest first)."""
        return sorted(self._store.values(), key=lambda f: f.created_at)

    def get_by_user(self, user_id: str) -> List[Feedback]:
        """Return all feedback entries submitted by *user_id* (oldest first)."""
        return sorted(
            (f for f in self._store.values() if f.user_id == user_id),
            key=lambda f: f.created_at,
        )

    def delete(self, feedback_id: str) -> bool:
        """Delete the feedback entry with *feedback_id*.

        Returns:
            True if the entry existed and was removed, False otherwise.
        """
        return self._store.pop(feedback_id, None) is not None

    def __len__(self) -> int:
        return len(self._store)
