"""Tests for user profile module and Flask endpoints."""

import pytest

import user_profile as up
from app import app as flask_app


@pytest.fixture(autouse=True)
def reset_profiles():
    """Ensure a clean profile store before every test."""
    up._reset()
    yield
    up._reset()


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# unit tests – user_profile module
# ---------------------------------------------------------------------------

class TestCreateProfile:
    def test_creates_profile_with_id(self):
        p = up.create_profile("Alice", "alice@example.com")
        assert p["id"] == 1
        assert p["name"] == "Alice"
        assert p["email"] == "alice@example.com"

    def test_ids_increment(self):
        p1 = up.create_profile("Alice", "alice@example.com")
        p2 = up.create_profile("Bob", "bob@example.com")
        assert p2["id"] == p1["id"] + 1

    def test_blank_name_raises(self):
        with pytest.raises(up.InvalidProfileDataError):
            up.create_profile("", "alice@example.com")

    def test_blank_email_raises(self):
        with pytest.raises(up.InvalidProfileDataError):
            up.create_profile("Alice", "")

    def test_invalid_email_raises(self):
        with pytest.raises(up.InvalidProfileDataError):
            up.create_profile("Alice", "not-an-email")

    def test_email_ending_with_dot_raises(self):
        with pytest.raises(up.InvalidProfileDataError):
            up.create_profile("Alice", "user@domain.")

    def test_email_dot_after_at_raises(self):
        with pytest.raises(up.InvalidProfileDataError):
            up.create_profile("Alice", "user@.com")


class TestGetProfile:
    def test_returns_existing_profile(self):
        p = up.create_profile("Alice", "alice@example.com")
        assert up.get_profile(p["id"]) == p

    def test_missing_id_raises(self):
        with pytest.raises(up.UserNotFoundError) as exc_info:
            up.get_profile(999)
        assert exc_info.value.user_id == 999


class TestUpdateProfile:
    def test_updates_fields(self):
        p = up.create_profile("Alice", "alice@example.com")
        updated = up.update_profile(p["id"], "Alicia", "alicia@example.com")
        assert updated["name"] == "Alicia"
        assert updated["email"] == "alicia@example.com"

    def test_missing_id_raises(self):
        with pytest.raises(up.UserNotFoundError):
            up.update_profile(999, "X", "x@example.com")

    def test_invalid_data_raises(self):
        p = up.create_profile("Alice", "alice@example.com")
        with pytest.raises(up.InvalidProfileDataError):
            up.update_profile(p["id"], "", "alice@example.com")


class TestDeleteProfile:
    def test_deletes_profile(self):
        p = up.create_profile("Alice", "alice@example.com")
        up.delete_profile(p["id"])
        with pytest.raises(up.UserNotFoundError):
            up.get_profile(p["id"])

    def test_missing_id_raises(self):
        with pytest.raises(up.UserNotFoundError):
            up.delete_profile(999)


class TestListProfiles:
    def test_empty_initially(self):
        assert up.list_profiles() == []

    def test_returns_all_profiles(self):
        up.create_profile("Alice", "alice@example.com")
        up.create_profile("Bob", "bob@example.com")
        assert len(up.list_profiles()) == 2


# ---------------------------------------------------------------------------
# integration tests – Flask routes
# ---------------------------------------------------------------------------

class TestIndexRoute:
    def test_returns_hello_world(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.get_json()["message"] == "Hello World"


class TestProfileRoutes:
    def test_list_profiles_empty(self, client):
        resp = client.get("/profiles")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_create_profile(self, client):
        resp = client.post("/profiles", json={"name": "Alice", "email": "alice@example.com"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Alice"
        assert data["id"] == 1

    def test_create_profile_missing_name_returns_400(self, client):
        resp = client.post("/profiles", json={"email": "alice@example.com"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_create_profile_invalid_email_returns_400(self, client):
        resp = client.post("/profiles", json={"name": "Alice", "email": "bad"})
        assert resp.status_code == 400

    def test_get_profile(self, client):
        client.post("/profiles", json={"name": "Alice", "email": "alice@example.com"})
        resp = client.get("/profiles/1")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Alice"

    def test_get_missing_profile_returns_404(self, client):
        resp = client.get("/profiles/999")
        assert resp.status_code == 404
        assert resp.get_json()["status"] == 404

    def test_update_profile(self, client):
        client.post("/profiles", json={"name": "Alice", "email": "alice@example.com"})
        resp = client.put("/profiles/1", json={"name": "Alicia", "email": "alicia@example.com"})
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Alicia"

    def test_update_missing_profile_returns_404(self, client):
        resp = client.put("/profiles/999", json={"name": "X", "email": "x@example.com"})
        assert resp.status_code == 404

    def test_delete_profile(self, client):
        client.post("/profiles", json={"name": "Alice", "email": "alice@example.com"})
        resp = client.delete("/profiles/1")
        assert resp.status_code == 204
        assert client.get("/profiles/1").status_code == 404

    def test_delete_missing_profile_returns_404(self, client):
        resp = client.delete("/profiles/999")
        assert resp.status_code == 404

    def test_unknown_route_returns_404_json(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404
        body = resp.get_json()
        assert body["status"] == 404
        assert "Content-Type" in resp.headers
        assert "application/json" in resp.headers["Content-Type"]
