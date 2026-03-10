#!/usr/bin/env python3
"""Tests for user_profile.py and the Flask app in app.py."""

import pytest

from user_profile import (
    DuplicateUsernameError,
    InvalidProfileDataError,
    UserNotFoundError,
    UserProfile,
    UserProfileStore,
)
from app import app as flask_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def store():
    """Return a fresh, empty UserProfileStore."""
    return UserProfileStore()


@pytest.fixture
def populated_store():
    """Return a store with two pre-created profiles."""
    s = UserProfileStore()
    s.create("alice", "alice@example.com", bio="Hello!")
    s.create("bob", "bob@example.com")
    return s


@pytest.fixture
def client(populated_store):
    """Return a Flask test client backed by a populated store."""
    import app as app_module

    original_store = app_module.store
    app_module.store = populated_store
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c
    app_module.store = original_store


# ---------------------------------------------------------------------------
# Unit tests: UserProfileStore
# ---------------------------------------------------------------------------


class TestCreate:
    def test_returns_user_profile(self, store):
        profile = store.create("alice", "alice@example.com")
        assert isinstance(profile, UserProfile)

    def test_assigns_incremental_ids(self, store):
        p1 = store.create("alice", "alice@example.com")
        p2 = store.create("bob", "bob@example.com")
        assert p1.id == 1
        assert p2.id == 2

    def test_stores_all_fields(self, store):
        profile = store.create("alice", "alice@example.com", bio="Hi", avatar_url="http://img")
        assert profile.username == "alice"
        assert profile.email == "alice@example.com"
        assert profile.bio == "Hi"
        assert profile.avatar_url == "http://img"

    def test_duplicate_username_raises(self, store):
        store.create("alice", "alice@example.com")
        with pytest.raises(DuplicateUsernameError):
            store.create("alice", "other@example.com")

    def test_empty_username_raises(self, store):
        with pytest.raises(InvalidProfileDataError):
            store.create("", "alice@example.com")

    def test_invalid_email_raises(self, store):
        with pytest.raises(InvalidProfileDataError):
            store.create("alice", "not-an-email")


class TestGet:
    def test_returns_correct_profile(self, populated_store):
        profile = populated_store.get(1)
        assert profile.username == "alice"

    def test_unknown_id_raises(self, populated_store):
        with pytest.raises(UserNotFoundError):
            populated_store.get(9999)

    def test_error_contains_id(self, populated_store):
        with pytest.raises(UserNotFoundError) as exc_info:
            populated_store.get(42)
        assert exc_info.value.user_id == 42


class TestListAll:
    def test_returns_list(self, populated_store):
        result = populated_store.list_all()
        assert isinstance(result, list)

    def test_returns_all_profiles(self, populated_store):
        assert len(populated_store.list_all()) == 2

    def test_empty_store_returns_empty_list(self, store):
        assert store.list_all() == []


class TestUpdate:
    def test_updates_username(self, populated_store):
        profile = populated_store.update(1, username="alicia")
        assert profile.username == "alicia"

    def test_updates_email(self, populated_store):
        profile = populated_store.update(1, email="new@example.com")
        assert profile.email == "new@example.com"

    def test_updates_bio(self, populated_store):
        profile = populated_store.update(1, bio="Updated bio")
        assert profile.bio == "Updated bio"

    def test_unknown_id_raises(self, populated_store):
        with pytest.raises(UserNotFoundError):
            populated_store.update(9999, username="x")

    def test_duplicate_username_raises(self, populated_store):
        with pytest.raises(DuplicateUsernameError):
            populated_store.update(1, username="bob")


class TestDelete:
    def test_removes_profile(self, populated_store):
        populated_store.delete(1)
        assert len(populated_store.list_all()) == 1

    def test_deleted_profile_not_retrievable(self, populated_store):
        populated_store.delete(1)
        with pytest.raises(UserNotFoundError):
            populated_store.get(1)

    def test_unknown_id_raises(self, populated_store):
        with pytest.raises(UserNotFoundError):
            populated_store.delete(9999)


class TestToDict:
    def test_to_dict_keys(self, store):
        profile = store.create("alice", "alice@example.com", bio="Hi")
        d = profile.to_dict()
        assert set(d.keys()) == {"id", "username", "email", "bio", "avatar_url"}

    def test_to_dict_values(self, store):
        profile = store.create("alice", "alice@example.com", bio="Hi")
        d = profile.to_dict()
        assert d["username"] == "alice"
        assert d["email"] == "alice@example.com"
        assert d["bio"] == "Hi"


# ---------------------------------------------------------------------------
# Integration tests: Flask app
# ---------------------------------------------------------------------------


class TestListProfilesEndpoint:
    def test_status_ok(self, client):
        assert client.get("/profiles").status_code == 200

    def test_returns_json(self, client):
        assert client.get("/profiles").content_type == "application/json"

    def test_profiles_key(self, client):
        data = client.get("/profiles").get_json()
        assert "profiles" in data

    def test_profiles_count(self, client):
        data = client.get("/profiles").get_json()
        assert len(data["profiles"]) == 2


class TestCreateProfileEndpoint:
    def test_creates_and_returns_201(self, client):
        resp = client.post("/profiles", json={"username": "carol", "email": "carol@example.com"})
        assert resp.status_code == 201

    def test_response_contains_id(self, client):
        data = client.post("/profiles", json={"username": "carol", "email": "carol@example.com"}).get_json()
        assert "id" in data

    def test_duplicate_username_returns_409(self, client):
        resp = client.post("/profiles", json={"username": "alice", "email": "x@example.com"})
        assert resp.status_code == 409

    def test_invalid_email_returns_400(self, client):
        resp = client.post("/profiles", json={"username": "newuser", "email": "bad-email"})
        assert resp.status_code == 400

    def test_empty_username_returns_400(self, client):
        resp = client.post("/profiles", json={"username": "", "email": "x@example.com"})
        assert resp.status_code == 400


class TestGetProfileEndpoint:
    def test_existing_profile_returns_200(self, client):
        assert client.get("/profiles/1").status_code == 200

    def test_existing_profile_data(self, client):
        data = client.get("/profiles/1").get_json()
        assert data["username"] == "alice"

    def test_missing_profile_returns_404(self, client):
        assert client.get("/profiles/9999").status_code == 404

    def test_missing_profile_error_key(self, client):
        data = client.get("/profiles/9999").get_json()
        assert "error" in data


class TestUpdateProfileEndpoint:
    def test_update_returns_200(self, client):
        resp = client.put("/profiles/1", json={"bio": "New bio"})
        assert resp.status_code == 200

    def test_update_changes_bio(self, client):
        client.put("/profiles/1", json={"bio": "Changed"})
        data = client.get("/profiles/1").get_json()
        assert data["bio"] == "Changed"

    def test_update_unknown_profile_returns_404(self, client):
        resp = client.put("/profiles/9999", json={"bio": "x"})
        assert resp.status_code == 404

    def test_update_duplicate_username_returns_409(self, client):
        resp = client.put("/profiles/1", json={"username": "bob"})
        assert resp.status_code == 409


class TestDeleteProfileEndpoint:
    def test_delete_returns_200(self, client):
        assert client.delete("/profiles/1").status_code == 200

    def test_delete_response_contains_id(self, client):
        data = client.delete("/profiles/1").get_json()
        assert data["deleted"] == 1

    def test_deleted_profile_no_longer_accessible(self, client):
        client.delete("/profiles/1")
        assert client.get("/profiles/1").status_code == 404

    def test_delete_unknown_profile_returns_404(self, client):
        assert client.delete("/profiles/9999").status_code == 404


class TestNotFoundHandler:
    def test_unknown_route_returns_404(self, client):
        assert client.get("/no-such-path").status_code == 404

    def test_unknown_route_returns_json(self, client):
        assert client.get("/no-such-path").content_type == "application/json"
