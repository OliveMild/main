import pytest
from user_profile import UserProfile, UserProfileError


def test_email_normalized_to_lowercase():
    profile = UserProfile(username="Alice_99", email="Alice@Example.COM")
    assert profile.email == "alice@example.com"


def test_username_stored_as_given():
    profile = UserProfile(username="Alice_99", email="alice@example.com")
    assert profile.username == "Alice_99"


def test_username_too_short_raises_error():
    with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
        UserProfile(username="x", email="alice@example.com")


def test_username_too_long_raises_error():
    with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
        UserProfile(username="a" * 31, email="alice@example.com")


def test_username_minimum_length():
    profile = UserProfile(username="abc", email="a@b.com")
    assert profile.username == "abc"


def test_username_maximum_length():
    profile = UserProfile(username="a" * 30, email="a@b.com")
    assert len(profile.username) == 30


def test_update_known_fields():
    profile = UserProfile(username="Alice_99", email="alice@example.com")
    profile.update(username="Bob_42", email="BOB@EXAMPLE.COM")
    assert profile.username == "Bob_42"
    assert profile.email == "bob@example.com"


def test_update_unknown_field_raises_error():
    profile = UserProfile(username="Alice_99", email="alice@example.com")
    with pytest.raises(UserProfileError, match="Unknown profile field\\(s\\): password"):
        profile.update(password="secret")


def test_update_username_too_short_raises_error():
    profile = UserProfile(username="Alice_99", email="alice@example.com")
    with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
        profile.update(username="x")


def test_update_email_normalized():
    profile = UserProfile(username="Alice_99", email="alice@example.com")
    profile.update(email="NEW@EXAMPLE.COM")
    assert profile.email == "new@example.com"
