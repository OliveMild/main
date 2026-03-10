"""Tests for the user_profile module."""

import pytest

from user_profile import UserProfile, UserProfileError


# ---------------------------------------------------------------------------
# UserProfile creation – happy paths
# ---------------------------------------------------------------------------


def test_create_profile_success():
    profile = UserProfile(username="alice", email="alice@example.com")
    assert profile.username == "alice"
    assert profile.email == "alice@example.com"
    assert profile.bio == ""


def test_create_profile_with_bio():
    profile = UserProfile(
        username="bob_99", email="bob@example.org", bio="Hello!"
    )
    assert profile.bio == "Hello!"


def test_email_stored_lowercase():
    profile = UserProfile(username="Carol", email="Carol@Example.COM")
    assert profile.email == "carol@example.com"


def test_username_stripped():
    profile = UserProfile(username="  dan  ", email="dan@example.com")
    assert profile.username == "dan"


# ---------------------------------------------------------------------------
# Username validation errors
# ---------------------------------------------------------------------------


def test_username_too_short():
    with pytest.raises(UserProfileError, match="3 and 30"):
        UserProfile(username="ab", email="x@x.com")


def test_username_too_long():
    with pytest.raises(UserProfileError, match="3 and 30"):
        UserProfile(username="a" * 31, email="x@x.com")


def test_username_invalid_characters():
    with pytest.raises(UserProfileError, match="letters, digits"):
        UserProfile(username="bad name!", email="x@x.com")


def test_username_not_a_string():
    with pytest.raises(UserProfileError, match="string"):
        UserProfile(username=123, email="x@x.com")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Email validation errors
# ---------------------------------------------------------------------------


def test_email_missing_at_sign():
    with pytest.raises(UserProfileError, match="valid email"):
        UserProfile(username="eve", email="notanemail")


def test_email_missing_domain():
    with pytest.raises(UserProfileError, match="valid email"):
        UserProfile(username="eve", email="eve@")


def test_email_not_a_string():
    with pytest.raises(UserProfileError, match="string"):
        UserProfile(username="eve", email=None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Bio validation errors
# ---------------------------------------------------------------------------


def test_bio_too_long():
    with pytest.raises(UserProfileError, match="200 characters"):
        UserProfile(username="frank", email="f@x.com", bio="x" * 201)


def test_bio_not_a_string():
    with pytest.raises(UserProfileError, match="string"):
        UserProfile(username="frank", email="f@x.com", bio=42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# update() – happy paths
# ---------------------------------------------------------------------------


def test_update_email():
    profile = UserProfile(username="grace", email="old@x.com")
    profile.update(email="new@x.com")
    assert profile.email == "new@x.com"


def test_update_bio():
    profile = UserProfile(username="heidi", email="h@x.com")
    profile.update(bio="Updated bio.")
    assert profile.bio == "Updated bio."


def test_update_username_and_bio():
    profile = UserProfile(username="ivan", email="i@x.com")
    profile.update(username="ivan_new", bio="New bio")
    assert profile.username == "ivan_new"
    assert profile.bio == "New bio"


# ---------------------------------------------------------------------------
# update() – error paths
# ---------------------------------------------------------------------------


def test_update_unknown_field():
    profile = UserProfile(username="judy", email="j@x.com")
    with pytest.raises(UserProfileError, match="Unknown profile field"):
        profile.update(password="secret")


def test_update_invalid_email():
    profile = UserProfile(username="karl", email="k@x.com")
    with pytest.raises(UserProfileError, match="valid email"):
        profile.update(email="not-valid")


# ---------------------------------------------------------------------------
# to_dict()
# ---------------------------------------------------------------------------


def test_to_dict():
    profile = UserProfile(
        username="lena", email="lena@x.com", bio="Hi there"
    )
    assert profile.to_dict() == {
        "username": "lena",
        "email": "lena@x.com",
        "bio": "Hi there",
    }
