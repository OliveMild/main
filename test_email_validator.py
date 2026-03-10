import pytest
from email_validator import is_valid_email, validate_email, InvalidEmailError


def test_is_valid_email_valid():
    assert is_valid_email("user@example.com") is True


def test_is_valid_email_invalid():
    assert is_valid_email("not-an-email") is False


def test_is_valid_email_double_at():
    assert is_valid_email("bad@@addr") is False


def test_validate_email_valid():
    assert validate_email("user@example.com") == "user@example.com"


def test_validate_email_invalid_raises():
    with pytest.raises(InvalidEmailError) as exc_info:
        validate_email("bad@@addr")
    assert "bad@@addr" in str(exc_info.value)


def test_is_valid_email_consecutive_dots_local():
    assert is_valid_email("user..name@example.com") is False


def test_is_valid_email_consecutive_dots_domain():
    assert is_valid_email("user@exam..ple.com") is False



    assert issubclass(InvalidEmailError, ValueError)
