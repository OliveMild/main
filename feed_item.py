import re
from datetime import datetime, timezone


class InvalidEmailError(ValueError):
    pass


_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


class FeedItem:
    def __init__(self, user_id: str, title: str, email: str, content: str = ""):
        if not _EMAIL_RE.match(email):
            raise InvalidEmailError(
                "email must be a valid email address (e.g. user@example.com)."
            )
        self.user_id = user_id
        self.title = title
        self.content = content
        self.email = email
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "email": self.email,
            "created_at": self.created_at,
        }
