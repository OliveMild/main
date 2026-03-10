#!/usr/bin/env python3
"""Tests for the user_profile module."""

import pytest
from user_profile import (
    InvalidProfileDataError,
    UserNotFoundError,
    UserProfile,
    UserProfileError,
    UserProfileStore,
)


def make_store():
    store = UserProfileStore()
    store.create("u1", "Alice", "alice@example.com", bio="Hello!")
    return store


# --- UserProfile ---


def test_user_profile_to_dict():
    p = UserProfile("u1", "Alice", "alice@example.com", bio="Hi")
    assert p.to_dict() == {
        "user_id": "u1",
        "name": "Alice",
        "email": "alice@example.com",
        "bio": "Hi",
    }


def test_user_profile_repr():
    p = UserProfile("u1", "Alice", "alice@example.com")
    assert "u1" in repr(p)
    assert "Alice" in repr(p)


# --- UserProfileStore.create ---


def test_create_returns_profile():
    store = UserProfileStore()
    profile = store.create("u1", "Alice", "alice@example.com")
    assert profile.user_id == "u1"
    assert profile.name == "Alice"
    assert profile.email == "alice@example.com"
    assert profile.bio == ""


def test_create_duplicate_raises():
    store = make_store()
    with pytest.raises(UserProfileError):
        store.create("u1", "Alice", "alice@example.com")


def test_create_empty_name_raises():
    store = UserProfileStore()
    with pytest.raises(InvalidProfileDataError) as exc:
        store.create("u2", "", "bob@example.com")
    assert exc.value.field == "name"


def test_create_empty_email_raises():
    store = UserProfileStore()
    with pytest.raises(InvalidProfileDataError) as exc:
        store.create("u2", "Bob", "")
    assert exc.value.field == "email"


def test_create_invalid_email_raises():
    store = UserProfileStore()
    with pytest.raises(InvalidProfileDataError) as exc:
        store.create("u2", "Bob", "not-an-email")
    assert exc.value.field == "email"


def test_create_email_missing_domain_raises():
    store = UserProfileStore()
    with pytest.raises(InvalidProfileDataError):
        store.create("u2", "Bob", "user@nodomain")


# --- UserProfileStore.get ---


def test_get_existing_profile():
    store = make_store()
    profile = store.get("u1")
    assert profile.name == "Alice"


def test_get_missing_profile_raises():
    store = UserProfileStore()
    with pytest.raises(UserNotFoundError) as exc:
        store.get("nonexistent")
    assert exc.value.user_id == "nonexistent"


# --- UserProfileStore.update ---


def test_update_name():
    store = make_store()
    profile = store.update("u1", name="Alicia")
    assert profile.name == "Alicia"


def test_update_email():
    store = make_store()
    profile = store.update("u1", email="alicia@example.com")
    assert profile.email == "alicia@example.com"


def test_update_missing_profile_raises():
    store = UserProfileStore()
    with pytest.raises(UserNotFoundError):
        store.update("nonexistent", name="X")


def test_update_invalid_email_raises():
    store = make_store()
    with pytest.raises(InvalidProfileDataError):
        store.update("u1", email="bad-email")


def test_update_bio_to_empty_string():
    store = make_store()
    profile = store.update("u1", bio="")
    assert profile.bio == ""


# --- UserProfileStore.delete ---


def test_delete_existing_profile():
    store = make_store()
    deleted = store.delete("u1")
    assert deleted.user_id == "u1"
    with pytest.raises(UserNotFoundError):
        store.get("u1")


def test_delete_missing_profile_raises():
    store = UserProfileStore()
    with pytest.raises(UserNotFoundError):
        store.delete("nonexistent")
