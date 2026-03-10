import pytest

from email_validator import is_valid_email
from user_registration import register_user


# ---------------------------------------------------------------------------
# is_valid_email — valid addresses
# ---------------------------------------------------------------------------

class TestValidEmails:
    def test_simple(self):
        assert is_valid_email("user@example.com") is True

    def test_subdomain(self):
        assert is_valid_email("user@mail.example.com") is True

    def test_plus_tag(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_dots_in_local(self):
        assert is_valid_email("first.last@example.com") is True

    def test_numeric_local(self):
        assert is_valid_email("123@example.com") is True

    def test_long_tld(self):
        assert is_valid_email("user@example.technology") is True

    def test_hyphen_in_domain(self):
        assert is_valid_email("user@my-domain.com") is True

    def test_uppercase(self):
        assert is_valid_email("User@Example.COM") is True

    def test_leading_and_trailing_whitespace_stripped(self):
        assert is_valid_email("  user@example.com  ") is True


# ---------------------------------------------------------------------------
# is_valid_email — invalid addresses
# ---------------------------------------------------------------------------

class TestInvalidEmails:
    def test_none(self):
        assert is_valid_email(None) is False

    def test_integer(self):
        assert is_valid_email(42) is False

    def test_list(self):
        assert is_valid_email(["user@example.com"]) is False

    def test_empty_string(self):
        assert is_valid_email("") is False

    def test_whitespace_only(self):
        assert is_valid_email("   ") is False

    def test_no_at_sign(self):
        assert is_valid_email("userexample.com") is False

    def test_multiple_at_signs(self):
        assert is_valid_email("user@@example.com") is False

    def test_consecutive_dots_local(self):
        assert is_valid_email("user..name@example.com") is False

    def test_consecutive_dots_domain(self):
        assert is_valid_email("user@example..com") is False

    def test_short_tld(self):
        assert is_valid_email("user@example.c") is False

    def test_leading_hyphen_domain(self):
        assert is_valid_email("user@-example.com") is False

    def test_trailing_hyphen_domain(self):
        assert is_valid_email("user@example-.com") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_missing_local(self):
        assert is_valid_email("@example.com") is False

    def test_plain_string(self):
        assert is_valid_email("not-an-email") is False


# ---------------------------------------------------------------------------
# register_user — success cases
# ---------------------------------------------------------------------------

class TestRegisterUserSuccess:
    def test_returns_success_dict(self):
        result = register_user("alice", "alice@example.com")
        assert result["success"] is True
        assert result["error"] is None
        assert result["username"] == "alice"
        assert result["email"] == "alice@example.com"

    def test_strips_whitespace_from_email(self):
        result = register_user("bob", "  bob@example.com  ")
        assert result["success"] is True
        assert result["email"] == "bob@example.com"

    def test_strips_whitespace_from_username(self):
        result = register_user("  carol  ", "carol@example.com")
        assert result["success"] is True
        assert result["username"] == "carol"


# ---------------------------------------------------------------------------
# register_user — failure cases
# ---------------------------------------------------------------------------

class TestRegisterUserFailure:
    def test_empty_username(self):
        result = register_user("", "alice@example.com")
        assert result["success"] is False
        assert result["error"] == "Username is required."

    def test_whitespace_username(self):
        result = register_user("   ", "alice@example.com")
        assert result["success"] is False
        assert result["error"] == "Username is required."

    def test_none_username(self):
        result = register_user(None, "alice@example.com")
        assert result["success"] is False
        assert result["error"] == "Username is required."

    def test_empty_email(self):
        result = register_user("alice", "")
        assert result["success"] is False
        assert result["error"] == "Email is required."

    def test_none_email(self):
        result = register_user("alice", None)
        assert result["success"] is False
        assert result["error"] == "Email is required."

    def test_invalid_email_does_not_echo_input(self):
        result = register_user("bob", "not-an-email")
        assert result["success"] is False
        assert result["error"] == "Invalid email address."
        assert "not-an-email" not in result["error"]

    def test_invalid_email_consecutive_dots(self):
        result = register_user("bob", "bob@example..com")
        assert result["success"] is False
        assert result["error"] == "Invalid email address."

    def test_invalid_email_no_at(self):
        result = register_user("bob", "bobexample.com")
        assert result["success"] is False
        assert result["error"] == "Invalid email address."
