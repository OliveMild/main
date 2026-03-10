#!/usr/bin/env python3
"""User feedback module for collecting and managing user feedback."""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


class ValidationError(ValueError):
    """Raised when feedback input fails validation."""


class FeedbackNotFoundError(KeyError):
    """Raised when a requested feedback item does not exist."""


@dataclass
class Feedback:
    """Represents a single piece of user feedback."""

    feedback_id: int
    name: str
    email: str
    rating: int
    comment: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """Return a dictionary representation of this feedback."""
        return {
            "feedback_id": self.feedback_id,
            "name": self.name,
            "email": self.email,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
        }


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("name must be a non-empty string")
    if len(name.strip()) > 100:
        raise ValidationError("name must be 100 characters or fewer")


def _validate_email(email: str) -> None:
    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        raise ValidationError(f"invalid email address: {email!r}")


def _validate_rating(rating: int) -> None:
    if not isinstance(rating, int) or isinstance(rating, bool):
        raise ValidationError("rating must be an integer")
    if rating < 1 or rating > 5:
        raise ValidationError("rating must be between 1 and 5 (inclusive)")


def _validate_comment(comment: str) -> None:
    if not isinstance(comment, str):
        raise ValidationError("comment must be a string")
    if len(comment) > 1000:
        raise ValidationError("comment must be 1000 characters or fewer")


class FeedbackStore:
    """In-memory store for user feedback entries."""

    def __init__(self) -> None:
        self._entries: List[Feedback] = []
        self._next_id: int = 1

    def submit(
        self,
        name: str,
        email: str,
        rating: int,
        comment: str = "",
    ) -> Feedback:
        """Validate inputs and store a new feedback entry.

        Args:
            name: Display name of the person submitting feedback.
            email: Contact email of the submitter.
            rating: Satisfaction score from 1 (lowest) to 5 (highest).
            comment: Optional free-text comment (max 1000 chars).

        Returns:
            The newly created :class:`Feedback` object.

        Raises:
            ValidationError: If any input fails validation.
        """
        _validate_name(name)
        _validate_email(email)
        _validate_rating(rating)
        _validate_comment(comment)

        entry = Feedback(
            feedback_id=self._next_id,
            name=name.strip(),
            email=email,
            rating=rating,
            comment=comment,
        )
        self._entries.append(entry)
        self._next_id += 1
        return entry

    def get(self, feedback_id: int) -> Feedback:
        """Return a feedback entry by its ID.

        Raises:
            FeedbackNotFoundError: If no entry with the given ID exists.
        """
        for entry in self._entries:
            if entry.feedback_id == feedback_id:
                return entry
        raise FeedbackNotFoundError(f"no feedback with id {feedback_id}")

    def all(self) -> List[Feedback]:
        """Return all feedback entries in submission order."""
        return list(self._entries)

    def filter_by_rating(self, rating: int) -> List[Feedback]:
        """Return all feedback entries that match the given rating.

        Raises:
            ValidationError: If *rating* is not a valid 1-5 integer.
        """
        _validate_rating(rating)
        return [e for e in self._entries if e.rating == rating]

    def average_rating(self) -> Optional[float]:
        """Return the mean rating across all entries, or *None* if empty."""
        if not self._entries:
            return None
        return sum(e.rating for e in self._entries) / len(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
