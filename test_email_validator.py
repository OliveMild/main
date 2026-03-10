import pytest
from email_validator import is_valid_email, validate_email, InvalidEmailError


class TestIsValidEmail:
    def test_valid_email(self):
        assert is_valid_email("user@example.com") is True

    def test_invalid_no_at(self):
        assert is_valid_email("not-an-email") is False

    def test_invalid_double_at(self):
        assert is_valid_email("bad@@addr") is False

    def test_valid_subdomain(self):
        assert is_valid_email("user@mail.example.co.uk") is True

    def test_valid_plus_addressing(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_invalid_no_domain(self):
        assert is_valid_email("user@") is False

    def test_invalid_no_tld(self):
        assert is_valid_email("user@example") is False

    def test_non_string(self):
        assert is_valid_email(None) is False


class TestValidateEmail:
    def test_returns_email_when_valid(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_raises_for_invalid(self):
        with pytest.raises(InvalidEmailError) as exc_info:
            validate_email("bad@@addr")
        assert "bad@@addr" in str(exc_info.value)

    def test_raises_for_plain_string(self):
        with pytest.raises(InvalidEmailError):
            validate_email("not-an-email")

    def test_error_is_value_error_subclass(self):
        with pytest.raises(ValueError):
            validate_email("bad")
