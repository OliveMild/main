class UserProfile:
    def __init__(self, username, email):
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        parts = email.split("@") if isinstance(email, str) else []
        if len(parts) != 2 or not parts[0] or not parts[1] or "." not in parts[1]:
            raise ValueError("Email must be a valid email address")
        self.username = username
        self.email = email

    def display(self):
        return f"User: {self.username}, Email: {self.email}"
