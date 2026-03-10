#!/usr/bin/env python3
"""Tests for user_feed module."""

import unittest

from user_feed import (
    CONTENT_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    FeedItemNotFoundError,
    FeedStore,
    InvalidContentError,
    InvalidTitleError,
    InvalidUserIdError,
    FeedItem,
    UserFeedError,
)


class TestExceptionHierarchy(unittest.TestCase):
    def test_invalid_user_id_is_user_feed_error(self):
        self.assertTrue(issubclass(InvalidUserIdError, UserFeedError))

    def test_invalid_content_is_user_feed_error(self):
        self.assertTrue(issubclass(InvalidContentError, UserFeedError))

    def test_invalid_title_is_user_feed_error(self):
        self.assertTrue(issubclass(InvalidTitleError, UserFeedError))

    def test_feed_item_not_found_is_user_feed_error(self):
        self.assertTrue(issubclass(FeedItemNotFoundError, UserFeedError))


class TestFeedItemConstruction(unittest.TestCase):
    def test_valid_construction(self):
        item = FeedItem(user_id="alice", title="My Post", content="Hello!")
        self.assertEqual(item.user_id, "alice")
        self.assertEqual(item.title, "My Post")
        self.assertEqual(item.content, "Hello!")

    def test_default_content_is_empty_string(self):
        item = FeedItem(user_id="bob", title="Post Title")
        self.assertEqual(item.content, "")

    def test_created_at_is_set(self):
        item = FeedItem(user_id="carol", title="A Title")
        self.assertIsNotNone(item.created_at)

    def test_user_id_with_underscores_and_digits(self):
        item = FeedItem(user_id="user_123", title="Post")
        self.assertEqual(item.user_id, "user_123")

    def test_title_exactly_max_length_is_valid(self):
        item = FeedItem(user_id="alice", title="x" * TITLE_MAX_LENGTH)
        self.assertEqual(len(item.title), TITLE_MAX_LENGTH)

    def test_content_exactly_max_length_is_valid(self):
        item = FeedItem(user_id="alice", title="Post", content="x" * CONTENT_MAX_LENGTH)
        self.assertEqual(len(item.content), CONTENT_MAX_LENGTH)


class TestFeedItemValidationErrors(unittest.TestCase):
    # --- user_id ---
    def test_empty_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            FeedItem(user_id="", title="Post")

    def test_none_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            FeedItem(user_id=None, title="Post")

    def test_user_id_with_spaces_raises(self):
        with self.assertRaises(InvalidUserIdError):
            FeedItem(user_id="bad user", title="Post")

    def test_user_id_too_long_raises(self):
        with self.assertRaises(InvalidUserIdError):
            FeedItem(user_id="a" * 65, title="Post")

    def test_user_id_exactly_64_chars_is_valid(self):
        item = FeedItem(user_id="a" * 64, title="Post")
        self.assertEqual(len(item.user_id), 64)

    # --- title ---
    def test_empty_title_raises(self):
        with self.assertRaises(InvalidTitleError):
            FeedItem(user_id="alice", title="")

    def test_none_title_raises(self):
        with self.assertRaises(InvalidTitleError):
            FeedItem(user_id="alice", title=None)

    def test_title_too_long_raises(self):
        with self.assertRaises(InvalidTitleError):
            FeedItem(user_id="alice", title="x" * (TITLE_MAX_LENGTH + 1))

    def test_non_string_title_raises(self):
        with self.assertRaises(InvalidTitleError):
            FeedItem(user_id="alice", title=42)

    # --- content ---
    def test_content_too_long_raises(self):
        with self.assertRaises(InvalidContentError):
            FeedItem(user_id="alice", title="Post", content="x" * (CONTENT_MAX_LENGTH + 1))

    def test_non_string_content_raises(self):
        with self.assertRaises(InvalidContentError):
            FeedItem(user_id="alice", title="Post", content=42)


class TestFeedItemSetters(unittest.TestCase):
    def setUp(self):
        self.item = FeedItem(user_id="alice", title="Original Title", content="original")

    def test_set_valid_title(self):
        self.item.title = "Updated Title"
        self.assertEqual(self.item.title, "Updated Title")

    def test_set_invalid_title_raises(self):
        with self.assertRaises(InvalidTitleError):
            self.item.title = ""

    def test_set_valid_content(self):
        self.item.content = "Updated content"
        self.assertEqual(self.item.content, "Updated content")

    def test_set_invalid_content_raises(self):
        with self.assertRaises(InvalidContentError):
            self.item.content = "x" * (CONTENT_MAX_LENGTH + 1)


class TestFeedItemToDict(unittest.TestCase):
    def test_to_dict_keys(self):
        item = FeedItem(user_id="alice", title="Post", content="Hello")
        d = item.to_dict()
        self.assertIn("user_id", d)
        self.assertIn("title", d)
        self.assertIn("content", d)
        self.assertIn("created_at", d)

    def test_to_dict_values(self):
        item = FeedItem(user_id="bob", title="News", content="Content here")
        d = item.to_dict()
        self.assertEqual(d["user_id"], "bob")
        self.assertEqual(d["title"], "News")
        self.assertEqual(d["content"], "Content here")


class TestFeedStore(unittest.TestCase):
    def setUp(self):
        self.store = FeedStore()

    def test_empty_store_len_is_zero(self):
        self.assertEqual(len(self.store), 0)

    def test_add_item_returns_feed_item(self):
        item = self.store.add_item("alice", "Post Title", "Some content")
        self.assertIsInstance(item, FeedItem)

    def test_add_item_increases_len(self):
        self.store.add_item("alice", "Post")
        self.assertEqual(len(self.store), 1)

    def test_get_all_returns_all_items(self):
        self.store.add_item("alice", "Post 1")
        self.store.add_item("bob", "Post 2", "Bob's content")
        items = self.store.get_all()
        self.assertEqual(len(items), 2)

    def test_get_all_is_copy(self):
        self.store.add_item("alice", "Post")
        items = self.store.get_all()
        items.clear()
        self.assertEqual(len(self.store), 1)

    def test_get_by_user_filters_correctly(self):
        self.store.add_item("alice", "Post 1")
        self.store.add_item("bob", "Post 2")
        self.store.add_item("alice", "Post 3", "Second post")
        alice_items = self.store.get_by_user("alice")
        self.assertEqual(len(alice_items), 2)
        for item in alice_items:
            self.assertEqual(item.user_id, "alice")

    def test_get_by_user_returns_empty_for_unknown_user(self):
        self.store.add_item("alice", "Post")
        result = self.store.get_by_user("unknown_user")
        self.assertEqual(result, [])

    def test_get_by_user_invalid_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            self.store.get_by_user("")

    def test_add_item_invalid_user_id_raises(self):
        with self.assertRaises(InvalidUserIdError):
            self.store.add_item("", "Post")

    def test_add_item_invalid_title_raises(self):
        with self.assertRaises(InvalidTitleError):
            self.store.add_item("alice", "")

    def test_add_item_invalid_content_raises(self):
        with self.assertRaises(InvalidContentError):
            self.store.add_item("alice", "Post", content=None)


if __name__ == "__main__":
    unittest.main()
