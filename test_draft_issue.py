"""Tests for draft_issue.py."""

import json
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

from draft_issue import create_draft_issue


class TestCreateDraftIssue(unittest.TestCase):
    """Unit tests for create_draft_issue."""

    def _make_response(self, data, status=201):
        response = MagicMock()
        response.__enter__ = lambda s: s
        response.__exit__ = MagicMock(return_value=False)
        response.read.return_value = json.dumps(data).encode()
        response.status = status
        return response

    @patch("draft_issue.urllib.request.urlopen")
    def test_creates_draft_issue_successfully(self, mock_urlopen):
        mock_response = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/1", "number": 1}
        )
        mock_urlopen.return_value = mock_response

        result = create_draft_issue("owner", "repo", "Test Issue", token="fake-token")

        self.assertEqual(result["number"], 1)
        self.assertIn("html_url", result)

    @patch("draft_issue.urllib.request.urlopen")
    def test_sends_correct_payload(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/2", "number": 2}
        )

        create_draft_issue("owner", "repo", "My Title", body="My body", token="tok")

        call_args = mock_urlopen.call_args
        request = call_args[0][0]
        payload = json.loads(request.data.decode())

        self.assertEqual(payload["title"], "My Title")
        self.assertEqual(payload["body"], "My body")
        # GitHub issues do not support a 'draft' field; verify it is not sent
        self.assertNotIn("draft", payload)

    @patch("draft_issue.urllib.request.urlopen")
    def test_uses_github_token_env_var(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/3", "number": 3}
        )

        with patch.dict("os.environ", {"GITHUB_TOKEN": "env-token"}):
            create_draft_issue("owner", "repo", "Title from env")

        request = mock_urlopen.call_args[0][0]
        self.assertIn("env-token", request.get_header("Authorization"))

    def test_raises_value_error_without_token(self):
        with patch.dict("os.environ", {}, clear=True):
            # Ensure GITHUB_TOKEN is not set
            import os
            os.environ.pop("GITHUB_TOKEN", None)
            with self.assertRaises(ValueError):
                create_draft_issue("owner", "repo", "No token")

    @patch("draft_issue.urllib.request.urlopen")
    def test_uses_correct_api_url(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/myorg/myrepo/issues/4", "number": 4}
        )

        create_draft_issue("myorg", "myrepo", "Title", token="tok")

        request = mock_urlopen.call_args[0][0]
        self.assertEqual(
            request.full_url,
            "https://api.github.com/repos/myorg/myrepo/issues",
        )


if __name__ == "__main__":
    unittest.main()
