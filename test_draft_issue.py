"""Tests for draft_issue.py."""

import json
import unittest
from unittest.mock import MagicMock, patch

from draft_issue import create_issue


class TestCreateIssue(unittest.TestCase):
    """Unit tests for create_issue."""

    def _make_response(self, data, status=201):
        response = MagicMock()
        response.__enter__ = lambda s: s
        response.__exit__ = MagicMock(return_value=False)
        response.read.return_value = json.dumps(data).encode()
        response.status = status
        return response

    @patch("draft_issue.urllib.request.urlopen")
    def test_creates_issue_successfully(self, mock_urlopen):
        mock_response = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/1", "number": 1}
        )
        mock_urlopen.return_value = mock_response

        result = create_issue("owner", "repo", "Test Issue", "", "fake-token")

        self.assertEqual(result["number"], 1)
        self.assertIn("html_url", result)

    @patch("draft_issue.urllib.request.urlopen")
    def test_sends_correct_payload(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/2", "number": 2}
        )

        create_issue("owner", "repo", "My Title", "My body", "tok")

        call_args = mock_urlopen.call_args
        request = call_args[0][0]
        payload = json.loads(request.data.decode())

        self.assertEqual(payload["title"], "My Title")
        self.assertEqual(payload["body"], "My body")

    @patch("draft_issue.urllib.request.urlopen")
    def test_uses_correct_api_url(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/myorg/myrepo/issues/4", "number": 4}
        )

        create_issue("myorg", "myrepo", "Title", "", "tok")

        request = mock_urlopen.call_args[0][0]
        self.assertEqual(
            request.full_url,
            "https://api.github.com/repos/myorg/myrepo/issues",
        )

    @patch("draft_issue.urllib.request.urlopen")
    def test_includes_auth_header(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"html_url": "https://github.com/owner/repo/issues/5", "number": 5}
        )

        create_issue("owner", "repo", "Title", "", "my-token")

        request = mock_urlopen.call_args[0][0]
        self.assertIn("my-token", request.get_header("Authorization"))


if __name__ == "__main__":
    unittest.main()
