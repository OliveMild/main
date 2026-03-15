import re

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9._%+\-]*[a-zA-Z0-9])?@"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def is_valid_email(email: object) -> bool:
    """Return True if *email* is a syntactically valid e-mail address.

    Rejects:
    - non-string values (including None)
    - empty or whitespace-only strings
    - consecutive dots anywhere in the address
    - multiple '@' characters
    - TLDs shorter than 2 characters
    - domain labels with leading or trailing hyphens
    """
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email:
        return False
    if ".." in email:
        return False
    if email.count("@") != 1:
        return False
    return bool(_EMAIL_REGEX.match(email))
