#!/usr/bin/env python3

from email_validator import validate_email, EmailNotValidError


class InvalidEmailError(EmailNotValidError):
    def __init__(self, email, reason):
        self.email = email
        super().__init__(f"Invalid email address: '{email}': {reason}")


def handle_error(exc):
    print(exc)


def validate_user_email(user_input):
    try:
        email = validate_email(user_input, check_deliverability=False)
        return email.normalized
    except EmailNotValidError as exc:
        raise InvalidEmailError(user_input, str(exc)) from exc


if __name__ == "__main__":
    print("Hello World")

    try:
        print(validate_user_email("test@example.com"))
    except InvalidEmailError as exc:
        handle_error(exc)

    try:
        print(validate_user_email("bad@@input"))
    except InvalidEmailError as exc:
        handle_error(exc)
