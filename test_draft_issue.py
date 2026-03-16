"""Tests for draft_issue.py."""

import json
import urllib.error
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

from draft_issue import create_draft_issue, main


class TestCreateDraftIssue(unittest.TestCase):
    """Unit tests for create_draft_issue()."""

    def _make_response(self, data: dict) -> MagicMock:
        body = json.dumps(data).encode()
        mock_resp = MagicMock()
        mock_resp.read.return_value = body
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("draft_issue.urllib.request.urlopen")
    def test_creates_issue_with_correct_payload(self, mock_urlopen):
        response_data = {
            "number": 42,
            "html_url": "https://github.com/owner/repo/issues/42",
            "title": "My draft",
        }
        mock_urlopen.return_value = self._make_response(response_data)

        result = create_draft_issue(
            token="tok",
            owner="owner",
            repo="repo",
            title="My draft",
            body="Some body",
        )

        self.assertEqual(result["number"], 42)
        self.assertEqual(result["html_url"], "https://github.com/owner/repo/issues/42")

        # Verify the request URL and payload
        call_args = mock_urlopen.call_args[0][0]
        self.assertEqual(call_args.full_url, "https://api.github.com/repos/owner/repo/issues")
        payload = json.loads(call_args.data.decode())
        self.assertEqual(payload["title"], "My draft")
        self.assertEqual(payload["body"], "Some body")
        self.assertIn("draft", payload["labels"])

    @patch("draft_issue.urllib.request.urlopen")
    def test_empty_body_is_allowed(self, mock_urlopen):
        mock_urlopen.return_value = self._make_response(
            {"number": 1, "html_url": "https://github.com/o/r/issues/1"}
        )
        result = create_draft_issue(token="tok", owner="o", repo="r", title="T")
        self.assertEqual(result["number"], 1)

    def test_raises_on_empty_token(self):
        with self.assertRaises(ValueError):
            create_draft_issue(token="", owner="o", repo="r", title="T")

    def test_raises_on_empty_owner(self):
        with self.assertRaises(ValueError):
            create_draft_issue(token="tok", owner="", repo="r", title="T")

    def test_raises_on_empty_repo(self):
        with self.assertRaises(ValueError):
            create_draft_issue(token="tok", owner="o", repo="", title="T")

    def test_raises_on_empty_title(self):
        with self.assertRaises(ValueError):
            create_draft_issue(token="tok", owner="o", repo="r", title="")

    @patch("draft_issue.urllib.request.urlopen")
    def test_http_error_propagates(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=BytesIO(b""),
        )
        with self.assertRaises(urllib.error.HTTPError):
            create_draft_issue(token="bad", owner="o", repo="r", title="T")


class TestMain(unittest.TestCase):
    """Unit tests for main()."""

    @patch("draft_issue.urllib.request.urlopen")
    def test_main_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(
            {"number": 7, "html_url": "https://github.com/o/r/issues/7"}
        ).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        rc = main(["--token", "tok", "--owner", "o", "--repo", "r", "--title", "My issue"])
        self.assertEqual(rc, 0)

    @patch("draft_issue.urllib.request.urlopen")
    def test_main_http_error_returns_1(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(b""),
        )
        rc = main(["--token", "tok", "--owner", "o", "--repo", "r", "--title", "T"])
        self.assertEqual(rc, 1)

    def test_main_missing_required_arg_exits(self):
        with self.assertRaises(SystemExit):
            main(["--token", "tok", "--owner", "o", "--repo", "r"])


if __name__ == "__main__":
    unittest.main()
