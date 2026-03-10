import pytest
from email_validator import is_valid_email, validate_email, EmailNotValidError, InvalidEmailError


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
        with pytest.raises(EmailNotValidError) as exc_info:
            validate_email("bad@@addr.com")
        msg = str(exc_info.value)
        assert "bad@@addr.com" in msg
        assert "The part after the @-sign contains invalid characters: '@'." in msg

    def test_raises_for_plain_string(self):
        with pytest.raises(EmailNotValidError):
            validate_email("not-an-email")

    def test_error_is_value_error_subclass(self):
        with pytest.raises(ValueError):
            validate_email("bad")

    def test_raises_for_non_string(self):
        with pytest.raises(EmailNotValidError):
            validate_email(None)

    def test_error_message_format(self):
        with pytest.raises(EmailNotValidError) as exc_info:
            validate_email("bad@@input")
        assert str(exc_info.value) == (
            "Invalid email address: 'bad@@input': "
            "The part after the @-sign contains invalid characters: '@'."
        )

    def test_error_message_missing_at(self):
        with pytest.raises(EmailNotValidError) as exc_info:
            validate_email("nodomain")
        assert "does not contain an @-sign" in str(exc_info.value)

    def test_error_message_no_domain(self):
        with pytest.raises(EmailNotValidError) as exc_info:
            validate_email("user@")
        assert "domain must not be empty" in str(exc_info.value)


class TestInvalidEmailErrorAlias:
    def test_invalid_email_error_is_alias(self):
        assert InvalidEmailError is EmailNotValidError

    def test_alias_can_be_used_to_catch(self):
        with pytest.raises(InvalidEmailError):
            validate_email("bad@@input")
