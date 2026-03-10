#!/usr/bin/env python3

import pytest
from user_profile import UserProfile, UserProfileStore, ProfileNotFoundError, ValidationError


class TestUserProfile:
    def test_create_valid_profile(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        assert profile.user_id == "u1"
        assert profile.name == "Alice"
        assert profile.email == "alice@example.com"
        assert profile.bio == ""

    def test_create_profile_with_bio(self):
        profile = UserProfile("u1", "Alice", "alice@example.com", bio="Hello!")
        assert profile.bio == "Hello!"

    def test_create_profile_strips_name_whitespace(self):
        profile = UserProfile("u1", "  Alice  ", "alice@example.com")
        assert profile.name == "Alice"

    def test_create_profile_empty_user_id_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("", "Alice", "alice@example.com")

    def test_create_profile_empty_name_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("u1", "", "alice@example.com")

    def test_create_profile_whitespace_name_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("u1", "   ", "alice@example.com")

    def test_create_profile_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("u1", "Alice", "not-an-email")

    def test_create_profile_malformed_email_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("u1", "Alice", "@example.com")

    def test_create_profile_incomplete_email_raises(self):
        with pytest.raises(ValidationError):
            UserProfile("u1", "Alice", "user@")

    def test_update_name(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        profile.update(name="Bob")
        assert profile.name == "Bob"

    def test_update_email(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        profile.update(email="alice2@example.com")
        assert profile.email == "alice2@example.com"

    def test_update_bio(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        profile.update(bio="New bio")
        assert profile.bio == "New bio"

    def test_update_empty_name_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(ValidationError):
            profile.update(name="  ")

    def test_update_invalid_email_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(ValidationError):
            profile.update(email="bad-email")

    def test_update_empty_email_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        with pytest.raises(ValidationError):
            profile.update(email="")

    def test_to_dict(self):
        profile = UserProfile("u1", "Alice", "alice@example.com", bio="Hi")
        d = profile.to_dict()
        assert d == {"user_id": "u1", "name": "Alice", "email": "alice@example.com", "bio": "Hi"}


class TestUserProfileStore:
    def setup_method(self):
        self.store = UserProfileStore()

    def test_add_and_get_profile(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        self.store.add(profile)
        retrieved = self.store.get("u1")
        assert retrieved.name == "Alice"

    def test_add_duplicate_raises(self):
        profile = UserProfile("u1", "Alice", "alice@example.com")
        self.store.add(profile)
        with pytest.raises(ValidationError):
            self.store.add(UserProfile("u1", "Bob", "bob@example.com"))

    def test_get_nonexistent_raises(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.get("nonexistent")

    def test_update_profile(self):
        self.store.add(UserProfile("u1", "Alice", "alice@example.com"))
        updated = self.store.update("u1", name="Alicia", email="alicia@example.com")
        assert updated.name == "Alicia"
        assert updated.email == "alicia@example.com"

    def test_update_nonexistent_raises(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.update("nonexistent", name="X")

    def test_delete_profile(self):
        self.store.add(UserProfile("u1", "Alice", "alice@example.com"))
        self.store.delete("u1")
        with pytest.raises(ProfileNotFoundError):
            self.store.get("u1")

    def test_delete_nonexistent_raises(self):
        with pytest.raises(ProfileNotFoundError):
            self.store.delete("nonexistent")

    def test_list_all_empty(self):
        assert self.store.list_all() == []

    def test_list_all(self):
        self.store.add(UserProfile("u1", "Alice", "alice@example.com"))
        self.store.add(UserProfile("u2", "Bob", "bob@example.com"))
        profiles = self.store.list_all()
        assert len(profiles) == 2
        user_ids = {p.user_id for p in profiles}
        assert user_ids == {"u1", "u2"}
