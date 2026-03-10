#!/usr/bin/env python3
"""Email validation module providing a reliable is_valid_email function."""

import re

# RFC 5321/5322 inspired regex for practical email validation:
# - Local part: alphanumeric and special chars, no leading/trailing/consecutive dots
# - @ separator
# - Domain: labels separated by dots, each label alphanumeric (hyphens allowed but
#   not at start/end of label), TLD at least 2 characters
_EMAIL_REGEX = re.compile(
    r"^(?!.*\.\.)"               # no consecutive dots anywhere
    r"(?!\.)"                    # local part must not start with a dot
    r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"  # local part characters
    r"(?<!\.)@"                  # local part must not end with a dot
    r"(?:[a-zA-Z0-9]"           # domain label start
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"  # domain label body
    r"\.)+"                      # dot separator after each label
    r"[a-zA-Z]{2,}$"            # TLD: at least 2 alpha characters
)


def is_valid_email(email: str) -> bool:
    """Return True if *email* is a valid email address, False otherwise.

    Validation rules:
    - Must contain exactly one '@' (enforced implicitly: '@' is not a valid local-part
      character, and the domain pattern only accepts alphanumerics and hyphens).
    - Local part must not start or end with a dot, and must not contain
      consecutive dots.
    - Domain must contain at least one dot, and the TLD must be at least two
      alpha characters long.
    - Total length must not exceed 254 characters (RFC 5321).
    """
    if not isinstance(email, str):
        return False
    if len(email) > 254:
        return False
    return bool(_EMAIL_REGEX.match(email))
