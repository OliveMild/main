import pytest
from email_validator import is_valid_email, validate_email, InvalidEmailError


class TestIsValidEmail:
    def test_simple_valid(self):
        assert is_valid_email("user@example.com") is True

    def test_plus_tag_subdomain(self):
        assert is_valid_email("user+tag@mail.example.co.uk") is True

    def test_none_returns_false(self):
        assert is_valid_email(None) is False

    def test_invalid_double_at(self):
        assert is_valid_email("bad@@addr") is False

    def test_missing_at(self):
        assert is_valid_email("notanemail") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_missing_local(self):
        assert is_valid_email("@example.com") is False

    def test_integer_returns_false(self):
        assert is_valid_email(42) is False

    def test_empty_string_returns_false(self):
        assert is_valid_email("") is False


class TestValidateEmail:
    def test_valid_returns_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_invalid_raises_error(self):
        with pytest.raises(InvalidEmailError, match="Invalid email address: 'bad@@addr'"):
            validate_email("bad@@addr")

    def test_none_raises_error(self):
        with pytest.raises(InvalidEmailError):
            validate_email(None)

    def test_error_is_value_error(self):
        with pytest.raises(ValueError):
            validate_email("bad@@addr")
