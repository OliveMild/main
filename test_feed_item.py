import pytest
from feed_item import FeedItem, InvalidEmailError


def test_to_dict_contains_expected_keys():
    item = FeedItem(user_id="alice", title="Post", email="alice@example.com")
    d = item.to_dict()
    assert d["user_id"] == "alice"
    assert d["title"] == "Post"
    assert d["content"] == ""
    assert d["email"] == "alice@example.com"
    assert "created_at" in d


def test_content_default_is_empty_string():
    item = FeedItem(user_id="bob", title="Hello", email="bob@example.com")
    assert item.to_dict()["content"] == ""


def test_content_can_be_set():
    item = FeedItem(user_id="bob", title="Hello", email="bob@example.com", content="Some text")
    assert item.to_dict()["content"] == "Some text"


def test_invalid_email_raises_error():
    with pytest.raises(InvalidEmailError):
        FeedItem(user_id="alice", title="Post", email="notanemail")


def test_invalid_email_missing_at_symbol():
    with pytest.raises(InvalidEmailError):
        FeedItem(user_id="alice", title="Post", email="aliceexample.com")


def test_invalid_email_missing_domain():
    with pytest.raises(InvalidEmailError):
        FeedItem(user_id="alice", title="Post", email="alice@")


def test_valid_email_accepted():
    item = FeedItem(user_id="carol", title="Test", email="carol@domain.org")
    assert item.email == "carol@domain.org"
