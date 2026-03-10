"""Tests for the feedback module."""

import importlib
import sys

import pytest


def reload_feedback():
    """Reload the feedback module to reset its state."""
    if "feedback" in sys.modules:
        del sys.modules["feedback"]
    return importlib.import_module("feedback")


def test_submit_and_average_single():
    feedback = reload_feedback()
    feedback.submit_feedback(5, "Great application!")
    assert feedback.get_average_rating() == 5.0


def test_submit_and_average_multiple():
    feedback = reload_feedback()
    feedback.submit_feedback(5, "Great application!")
    feedback.submit_feedback(3)
    assert feedback.get_average_rating() == 4.0


def test_average_no_feedback():
    feedback = reload_feedback()
    assert feedback.get_average_rating() == 0.0


def test_submit_without_message():
    feedback = reload_feedback()
    feedback.submit_feedback(4)
    assert feedback.get_average_rating() == 4.0


def test_average_with_sequential_ratings():
    feedback = reload_feedback()
    feedback.submit_feedback(1)
    feedback.submit_feedback(2)
    feedback.submit_feedback(3)
    assert feedback.get_average_rating() == 2.0


def test_invalid_rating_type():
    feedback = reload_feedback()
    with pytest.raises(ValueError):
        feedback.submit_feedback("five")


def test_invalid_rating_out_of_range():
    feedback = reload_feedback()
    with pytest.raises(ValueError):
        feedback.submit_feedback(6)
    with pytest.raises(ValueError):
        feedback.submit_feedback(0)
