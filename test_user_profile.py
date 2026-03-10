import os
import tempfile
import unittest

import user_profile as up


class TestUserProfile(unittest.TestCase):
    def setUp(self):
        fd, self._tmp = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self._tmp)  # start without the file

    def tearDown(self):
        if os.path.exists(self._tmp):
            os.remove(self._tmp)

    # --- create_profile ---

    def test_create_profile_returns_dict(self):
        profile = up.create_profile("Alice", "alice@example.com", path=self._tmp)
        self.assertEqual(profile, {"name": "Alice", "email": "alice@example.com"})

    def test_create_profile_persists_file(self):
        up.create_profile("Bob", "bob@example.com", path=self._tmp)
        self.assertTrue(os.path.exists(self._tmp))

    def test_create_profile_empty_name_raises(self):
        with self.assertRaises(ValueError) as ctx:
            up.create_profile("", "alice@example.com", path=self._tmp)
        self.assertIn("name must not be empty", str(ctx.exception))

    def test_create_profile_invalid_email_raises(self):
        with self.assertRaises(ValueError) as ctx:
            up.create_profile("Alice", "@bad", path=self._tmp)
        self.assertIn("email must be a valid email address", str(ctx.exception))

    # --- load_profile ---

    def test_load_profile_returns_saved_data(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        profile = up.load_profile(path=self._tmp)
        self.assertEqual(profile["name"], "Alice")
        self.assertEqual(profile["email"], "alice@example.com")

    def test_load_profile_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            up.load_profile(path=self._tmp)

    # --- update_profile ---

    def test_update_profile_name(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        updated = up.update_profile({"name": "Alice Smith"}, path=self._tmp)
        self.assertEqual(updated["name"], "Alice Smith")
        self.assertEqual(updated["email"], "alice@example.com")

    def test_update_profile_email(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        updated = up.update_profile({"email": "new@example.com"}, path=self._tmp)
        self.assertEqual(updated["email"], "new@example.com")

    def test_update_profile_persists_change(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        up.update_profile({"name": "Alice Smith"}, path=self._tmp)
        profile = up.load_profile(path=self._tmp)
        self.assertEqual(profile["name"], "Alice Smith")

    def test_update_profile_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            up.update_profile({"name": "Ghost"}, path=self._tmp)

    def test_update_profile_empty_name_raises(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        with self.assertRaises(ValueError) as ctx:
            up.update_profile({"name": ""}, path=self._tmp)
        self.assertIn("name must not be empty", str(ctx.exception))

    def test_update_profile_invalid_email_raises(self):
        up.create_profile("Alice", "alice@example.com", path=self._tmp)
        with self.assertRaises(ValueError) as ctx:
            up.update_profile({"email": "notvalid"}, path=self._tmp)
        self.assertIn("email must be a valid email address", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
