#!/usr/bin/env python3
"""Tests for the user_profile module."""

import pytest

from user_profile import UserProfile, UserProfileNotFoundError, UserProfileStore


def make_store():
    store = UserProfileStore()
    store.add(UserProfile("u1", "Alice", "alice@example.com", "Hello, I'm Alice."))
    store.add(UserProfile("u2", "Bob", "bob@example.com"))
    return store


def test_get_existing_profile():
    store = make_store()
    profile = store.get("u1")
    assert profile.name == "Alice"
    assert profile.email == "alice@example.com"
    assert profile.bio == "Hello, I'm Alice."


def test_get_missing_profile_raises_error():
    store = make_store()
    with pytest.raises(UserProfileNotFoundError):
        store.get("unknown")


def test_add_and_retrieve_profile():
    store = UserProfileStore()
    profile = UserProfile("u3", "Carol", "carol@example.com")
    store.add(profile)
    assert store.get("u3").name == "Carol"


def test_update_profile():
    store = make_store()
    updated = store.update("u1", bio="Updated bio.")
    assert updated.bio == "Updated bio."
    assert store.get("u1").bio == "Updated bio."


def test_update_missing_profile_raises_error():
    store = make_store()
    with pytest.raises(UserProfileNotFoundError):
        store.update("unknown", bio="Should fail.")


def test_update_invalid_attribute_raises_error():
    store = make_store()
    with pytest.raises(AttributeError):
        store.update("u1", nonexistent_field="value")


def test_update_user_id_raises_error():
    store = make_store()
    # user_id is a positional-only positional argument in update(); passing it
    # as a keyword argument raises TypeError, preventing accidental id changes.
    with pytest.raises(TypeError):
        store.update("u1", user_id="new_id")


def test_delete_profile():
    store = make_store()
    store.delete("u2")
    with pytest.raises(UserProfileNotFoundError):
        store.get("u2")


def test_delete_missing_profile_raises_error():
    store = make_store()
    with pytest.raises(UserProfileNotFoundError):
        store.delete("unknown")


def test_bio_defaults_to_empty_string():
    profile = UserProfile("u4", "Dave", "dave@example.com")
    assert profile.bio == ""


def test_to_dict():
    profile = UserProfile("u1", "Alice", "alice@example.com", "Bio text.")
    d = profile.to_dict()
    assert d == {
        "user_id": "u1",
        "name": "Alice",
        "email": "alice@example.com",
        "bio": "Bio text.",
    }


def test_all_profiles():
    store = make_store()
    profiles = store.all()
    assert len(profiles) == 2


def test_repr():
    profile = UserProfile("u1", "Alice", "alice@example.com")
    assert "u1" in repr(profile)
    assert "Alice" in repr(profile)
