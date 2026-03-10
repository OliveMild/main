#!/usr/bin/env python3

import pytest
from user_profile import (
    InvalidFieldError,
    UserNotFoundError,
    UserProfile,
    UserProfileError,
    UserProfileStore,
)


class TestUserProfile:
    def test_create_valid_profile(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        assert profile.user_id == "u1"
        assert profile.name == "Alice"
        assert profile.email == "alice@example.com"
        assert profile.age is None
        assert profile.bio == ""

    def test_create_profile_with_all_fields(self):
        profile = UserProfile("u2", "Bob", "bob@example.com", age=30, bio="Hello")
        assert profile.age == 30
        assert profile.bio == "Hello"

    def test_empty_user_id_raises(self):
        with pytest.raises(UserProfileError):
            UserProfile("", "Alice", "alice@example.com")

    def test_empty_name_raises(self):
        with pytest.raises(UserProfileError):
            UserProfile("u1", "", "alice@example.com")

    def test_invalid_email_raises(self):
        with pytest.raises(UserProfileError):
            UserProfile("u1", "Alice", "not-an-email")

    def test_negative_age_raises(self):
        with pytest.raises(UserProfileError):
            UserProfile("u1", "Alice", "alice@example.com", age=-1)

    def test_non_integer_age_raises(self):
        with pytest.raises(UserProfileError):
            UserProfile("u1", "Alice", "alice@example.com", age="thirty")

    def test_update_valid_fields(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        profile.update(name="Alicia", bio="Updated bio")
        assert profile.name == "Alicia"
        assert profile.bio == "Updated bio"

    def test_update_invalid_field_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(InvalidFieldError):
            profile.update(username="alice123")

    def test_update_invalid_email_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(UserProfileError):
            profile.update(email="bad-email")

    def test_update_invalid_age_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(UserProfileError):
            profile.update(age=-5)

    def test_to_dict(self):
        profile = UserProfile("u1", "Alice", "alice@example.com", age=25, bio="Hi")
        d = profile.to_dict()
        assert d == {
            "user_id": "u1",
            "name": "Alice",
            "email": "alice@example.com",
            "age": 25,
            "bio": "Hi",
        }

    def test_repr(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        assert "u1" in repr(profile)
        assert "Alice" in repr(profile)


class TestUserProfileStore:
    def test_add_and_get(self):
        store = UserProfileStore()
        profile = UserProfile("u1", "Alice", "alice@example.com")
        store.add(profile)
        retrieved = store.get("u1")
        assert retrieved is profile

    def test_get_nonexistent_raises(self):
        store = UserProfileStore()
        with pytest.raises(UserNotFoundError):
            store.get("nonexistent")

    def test_delete(self):
        store = UserProfileStore()
        profile = UserProfile("u1", "Alice", "alice@example.com")
        store.add(profile)
        store.delete("u1")
        with pytest.raises(UserNotFoundError):
            store.get("u1")

    def test_delete_nonexistent_raises(self):
        store = UserProfileStore()
        with pytest.raises(UserNotFoundError):
            store.delete("nonexistent")

    def test_all_returns_all_profiles(self):
        store = UserProfileStore()
        p1 = UserProfile("u1", "Alice", "alice@example.com")
        p2 = UserProfile("u2", "Bob", "bob@example.com")
        store.add(p1)
        store.add(p2)
        profiles = store.all()
        assert len(profiles) == 2
        assert p1 in profiles
        assert p2 in profiles

    def test_add_non_profile_raises(self):
        store = UserProfileStore()
        with pytest.raises(UserProfileError):
            store.add({"user_id": "u1"})
