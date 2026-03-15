#!/usr/bin/env python3
"""User feed module: creation, validation, and retrieval of feed items."""

import re
from datetime import datetime, timezone


class UserFeedError(Exception):
    """Base exception for user feed errors."""


class InvalidUserIdError(UserFeedError):
    """Raised when a user ID is invalid."""


class InvalidContentError(UserFeedError):
    """Raised when feed item content is invalid."""


class InvalidTitleError(UserFeedError):
    """Raised when a feed item title is invalid."""


class FeedItemNotFoundError(UserFeedError):
    """Raised when a requested feed item does not exist."""


_USER_ID_RE = re.compile(r'^[A-Za-z0-9_]{1,64}$')

CONTENT_MAX_LENGTH = 2000
TITLE_MAX_LENGTH = 200


def _validate_user_id(user_id):
    if not isinstance(user_id, str) or not _USER_ID_RE.match(user_id):
        raise InvalidUserIdError(
            "user_id must be a non-empty string of up to 64 alphanumeric "
            "characters or underscores."
        )


def _validate_title(title):
    if not isinstance(title, str):
        raise InvalidTitleError("title must be a string.")
    if len(title) == 0:
        raise InvalidTitleError("title must not be empty.")
    if len(title) > TITLE_MAX_LENGTH:
        raise InvalidTitleError(
            f"title must not exceed {TITLE_MAX_LENGTH} characters."
        )


def _validate_content(content):
    if not isinstance(content, str):
        raise InvalidContentError("content must be a string.")
    if len(content) > CONTENT_MAX_LENGTH:
        raise InvalidContentError(
            f"content must not exceed {CONTENT_MAX_LENGTH} characters."
        )


class FeedItem:
    """Represents a single item in a user's feed."""

    def __init__(self, user_id, title, content=""):
        _validate_user_id(user_id)
        _validate_title(title)
        _validate_content(content)
        self._user_id = user_id
        self._title = title
        self._content = content
        self._created_at = datetime.now(timezone.utc)

    @property
    def user_id(self):
        return self._user_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        _validate_title(value)
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        _validate_content(value)
        self._content = value

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self):
        """Return a plain-dict serialisation of this feed item."""
        return {
            "user_id": self._user_id,
            "title": self._title,
            "content": self._content,
            "created_at": self._created_at.isoformat(),
        }

    def __repr__(self):
        return (
            f"FeedItem(user_id={self._user_id!r}, "
            f"title={self._title!r}, content={self._content!r})"
        )


class FeedStore:
    """In-memory store for FeedItem objects."""

    def __init__(self):
        self._items = []

    def add_item(self, user_id, title, content=""):
        """Create and store a new feed item; returns the item."""
        item = FeedItem(user_id=user_id, title=title, content=content)
        self._items.append(item)
        return item

    def get_all(self):
        """Return a copy of all stored feed items."""
        return list(self._items)

    def get_by_user(self, user_id):
        """Return all feed items belonging to *user_id*."""
        _validate_user_id(user_id)
        return [item for item in self._items if item.user_id == user_id]

    def __len__(self):
        return len(self._items)
