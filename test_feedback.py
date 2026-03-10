"""Tests for the feedback module."""
import pytest
import feedback


@pytest.fixture(autouse=True)
def reset_feedbacks():
    """Reset the feedbacks list before each test."""
    feedback._feedbacks.clear()
    yield
    feedback._feedbacks.clear()


def test_submit_feedback_with_comment():
    feedback.submit_feedback(5, "Great application!")
    assert feedback._feedbacks == [{"rating": 5, "comment": "Great application!"}]


def test_submit_feedback_without_comment():
    feedback.submit_feedback(3)
    assert feedback._feedbacks == [{"rating": 3, "comment": None}]


def test_get_average_rating_no_feedbacks():
    assert feedback.get_average_rating() is None


def test_get_average_rating_single():
    feedback.submit_feedback(4)
    assert feedback.get_average_rating() == 4.0


def test_get_average_rating_multiple():
    feedback.submit_feedback(5, "Great application!")
    feedback.submit_feedback(3)
    assert feedback.get_average_rating() == 4.0


def test_get_average_rating_example():
    feedback.submit_feedback(4, "Works well")
    feedback.submit_feedback(5)
    assert feedback.get_average_rating() == 4.5


def test_submit_feedback_invalid_rating():
    with pytest.raises(TypeError):
        feedback.submit_feedback("excellent")
