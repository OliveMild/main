#!/usr/bin/env python3
"""Tests for the email_validator module."""

import pytest

from email_validator import InvalidEmailError, is_valid_email, validate_email


# ---------------------------------------------------------------------------
# is_valid_email — valid addresses
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.org",
        "user_name@sub.domain.com",
        "u@example.co.uk",
        "firstname.lastname@company.io",
        "test123@test456.net",
        "a@b.co",
    ],
)
def test_valid_emails(email):
    assert is_valid_email(email) is True


# ---------------------------------------------------------------------------
# is_valid_email — invalid addresses
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "email",
    [
        "",                          # empty string
        "plainaddress",              # missing @
        "@nodomain.com",             # missing local part
        "user@",                     # missing domain
        "user@.com",                 # domain starts with dot
        "user@com",                  # TLD only (no dot in domain)
        "user@@example.com",         # double @
        "user @example.com",         # space in local part
        "user@ example.com",         # space in domain
        None,                        # not a string
        123,                         # not a string
        "a" * 65 + "@example.com",   # local part > 64 chars
        "user@" + "a" * 250 + ".com",  # total length > 254
    ],
)
def test_invalid_emails(email):
    assert is_valid_email(email) is False


# ---------------------------------------------------------------------------
# validate_email
# ---------------------------------------------------------------------------


def test_validate_email_returns_email_when_valid():
    email = "user@example.com"
    assert validate_email(email) == email


def test_validate_email_raises_for_invalid():
    with pytest.raises(InvalidEmailError):
        validate_email("not-an-email")


def test_validate_email_error_message_contains_address():
    bad_email = "bad@@address"
    with pytest.raises(InvalidEmailError, match="bad@@address"):
        validate_email(bad_email)


def test_validate_email_raises_invalid_email_error_subclass_of_value_error():
    with pytest.raises(ValueError):
        validate_email("missing-at-sign")
