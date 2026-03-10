import pytest
from email_validator import InvalidEmailError, is_valid_email, validate_email


class TestIsValidEmail:
    def test_valid_simple(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_plus_tag_subdomain(self):
        assert is_valid_email("user+tag@mail.example.co.uk") is True

    def test_none_returns_false(self):
        assert is_valid_email(None) is False

    def test_invalid_double_at(self):
        assert is_valid_email("bad@@addr") is False

    def test_invalid_no_at(self):
        assert is_valid_email("notanemail") is False

    def test_non_string_returns_false(self):
        assert is_valid_email(42) is False


class TestValidateEmail:
    def test_valid_returns_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_invalid_raises(self):
        with pytest.raises(InvalidEmailError, match="Invalid email address: 'bad@@addr'"):
            validate_email("bad@@addr")

    def test_invalid_error_is_value_error(self):
        with pytest.raises(ValueError):
            validate_email("bad@@addr")
