import pytest

from user_profile import UserProfile, UserProfileError


class TestUserProfileCreation:
    def test_email_normalized_to_lowercase(self):
        profile = UserProfile(username="Alice_99", email="Alice@Example.COM")
        assert profile.email == "alice@example.com"

    def test_username_stored_as_given(self):
        profile = UserProfile(username="Alice_99", email="Alice@Example.COM")
        assert profile.username == "Alice_99"

    def test_username_too_short_raises(self):
        with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
            UserProfile(username="x", email="alice@example.com")

    def test_username_too_long_raises(self):
        with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
            UserProfile(username="a" * 31, email="alice@example.com")

    def test_username_minimum_length_allowed(self):
        profile = UserProfile(username="abc", email="test@test.com")
        assert profile.username == "abc"

    def test_username_maximum_length_allowed(self):
        profile = UserProfile(username="a" * 30, email="test@test.com")
        assert profile.username == "a" * 30


class TestUserProfileUpdate:
    def setup_method(self):
        self.profile = UserProfile(username="Alice_99", email="alice@example.com")

    def test_update_unknown_field_raises(self):
        with pytest.raises(UserProfileError, match="Unknown profile field\\(s\\): password"):
            self.profile.update(password="secret")

    def test_update_multiple_unknown_fields_raises(self):
        with pytest.raises(UserProfileError, match="Unknown profile field\\(s\\):"):
            self.profile.update(password="secret", age=25)

    def test_update_email_normalizes(self):
        self.profile.update(email="NEW@EXAMPLE.COM")
        assert self.profile.email == "new@example.com"

    def test_update_username_valid(self):
        self.profile.update(username="Bob_42")
        assert self.profile.username == "Bob_42"

    def test_update_username_too_short_raises(self):
        with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
            self.profile.update(username="xy")

    def test_update_username_too_long_raises(self):
        with pytest.raises(UserProfileError, match="Username must be between 3 and 30 characters."):
            self.profile.update(username="a" * 31)
