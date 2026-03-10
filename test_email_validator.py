import pytest
from email_validator import is_valid_email, validate_email, InvalidEmailError


class TestIsValidEmail:
    def test_valid_simple(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_subdomain(self):
        assert is_valid_email("user@mail.example.co.uk") is True

    def test_valid_plus_addressing(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_valid_numeric_local(self):
        assert is_valid_email("123@example.com") is True

    def test_invalid_missing_at(self):
        assert is_valid_email("not-an-email") is False

    def test_invalid_double_at(self):
        assert is_valid_email("bad@@addr.com") is False

    def test_invalid_no_domain(self):
        assert is_valid_email("user@") is False

    def test_invalid_no_tld(self):
        assert is_valid_email("user@example") is False

    def test_invalid_single_char_tld(self):
        assert is_valid_email("user@example.c") is False

    def test_invalid_non_string(self):
        assert is_valid_email(None) is False

    def test_invalid_integer(self):
        assert is_valid_email(42) is False


class TestValidateEmail:
    def test_returns_email_when_valid(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_raises_for_double_at(self):
        with pytest.raises(InvalidEmailError) as exc_info:
            validate_email("bad@@addr.com")
        assert "bad@@addr.com" in str(exc_info.value)

    def test_raises_for_plain_string(self):
        with pytest.raises(InvalidEmailError):
            validate_email("not-an-email")

    def test_error_is_value_error_subclass(self):
        with pytest.raises(ValueError):
            validate_email("bad")

    def test_raises_for_non_string(self):
        with pytest.raises(InvalidEmailError):
            validate_email(None)
