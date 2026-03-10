#!/usr/bin/env python3
"""Tests for the custom error handlers module."""

import unittest
from error_handlers import (
    AppError,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    handle_error,
    safe_call,
)


class TestAppError(unittest.TestCase):
    def test_message_and_code(self):
        err = AppError("something went wrong", code=500)
        self.assertEqual(err.message, "something went wrong")
        self.assertEqual(err.code, 500)

    def test_str_with_code(self):
        err = AppError("oops", code=42)
        self.assertEqual(str(err), "[42] oops")

    def test_str_without_code(self):
        err = AppError("plain error")
        self.assertEqual(str(err), "plain error")


class TestNotFoundError(unittest.TestCase):
    def test_default_message(self):
        err = NotFoundError()
        self.assertEqual(err.message, "Resource not found")
        self.assertEqual(err.code, 404)

    def test_custom_message(self):
        err = NotFoundError("User not found")
        self.assertEqual(err.message, "User not found")

    def test_is_app_error(self):
        self.assertIsInstance(NotFoundError(), AppError)


class TestValidationError(unittest.TestCase):
    def test_default_message(self):
        err = ValidationError()
        self.assertEqual(err.message, "Validation failed")
        self.assertEqual(err.code, 400)

    def test_custom_message(self):
        err = ValidationError("Email is invalid")
        self.assertEqual(err.message, "Email is invalid")


class TestUnauthorizedError(unittest.TestCase):
    def test_default_message(self):
        err = UnauthorizedError()
        self.assertEqual(err.message, "Unauthorized")
        self.assertEqual(err.code, 401)

    def test_custom_message(self):
        err = UnauthorizedError("Token expired")
        self.assertEqual(err.message, "Token expired")


class TestHandleError(unittest.TestCase):
    def test_app_error(self):
        response = handle_error(AppError("bad request", code=400))
        self.assertEqual(response, {"error": "bad request", "code": 400})

    def test_not_found_error(self):
        response = handle_error(NotFoundError("Missing"))
        self.assertEqual(response, {"error": "Missing", "code": 404})

    def test_generic_exception(self):
        response = handle_error(ValueError("unexpected"))
        self.assertEqual(response, {"error": "unexpected", "code": 500})


class TestSafeCall(unittest.TestCase):
    def test_success(self):
        result, err = safe_call(lambda x: x * 2, 3)
        self.assertEqual(result, 6)
        self.assertIsNone(err)

    def test_app_error(self):
        def fail():
            raise NotFoundError("not here")

        result, err = safe_call(fail)
        self.assertIsNone(result)
        self.assertEqual(err, {"error": "not here", "code": 404})

    def test_generic_exception(self):
        def boom():
            raise RuntimeError("crash")

        result, err = safe_call(boom)
        self.assertIsNone(result)
        self.assertEqual(err, {"error": "crash", "code": 500})


if __name__ == "__main__":
    unittest.main()
