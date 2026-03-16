"""Tests for draft_issue.py"""

import json
import unittest
from io import BytesIO
from unittest.mock import MagicMock, call, patch

import draft_issue


def _make_response(payload, status=200):
    """Return a mock response object compatible with urllib.request.urlopen."""
    mock = MagicMock()
    mock.read.return_value = json.dumps(payload).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


class TestCreateDraftIssue(unittest.TestCase):
    @patch("draft_issue.urllib.request.urlopen")
    def test_creates_issue_with_draft_label(self, mock_urlopen):
        label_response = _make_response({"name": "draft", "color": "d3d3d3"})
        issue_response = _make_response(
            {"number": 42, "html_url": "https://github.com/o/r/issues/42", "labels": [{"name": "draft"}]}
        )
        mock_urlopen.side_effect = [label_response, issue_response]

        result = draft_issue.create_draft_issue("o", "r", "My draft", token="tok")

        self.assertEqual(result["number"], 42)
        # Second call should POST to /repos/o/r/issues
        post_call = mock_urlopen.call_args_list[1]
        req = post_call[0][0]
        self.assertIn("/repos/o/r/issues", req.full_url)
        body = json.loads(req.data)
        self.assertIn("draft", body["labels"])
        self.assertEqual(body["title"], "My draft")

    @patch("draft_issue.urllib.request.urlopen")
    def test_creates_draft_label_when_missing(self, mock_urlopen):
        import urllib.error

        not_found = urllib.error.HTTPError(None, 404, "Not Found", {}, None)
        label_create_response = _make_response({"name": "draft"})
        issue_response = _make_response({"number": 1, "html_url": "u", "labels": []})
        mock_urlopen.side_effect = [not_found, label_create_response, issue_response]

        draft_issue.create_draft_issue("o", "r", "title", token="tok")

        # Should make 3 calls: GET label (404), POST label, POST issue
        self.assertEqual(mock_urlopen.call_count, 3)

    def test_raises_without_token(self):
        import os

        env = os.environ.copy()
        os.environ.pop("GITHUB_TOKEN", None)
        try:
            with self.assertRaises(ValueError):  # no token provided
                draft_issue.create_draft_issue("o", "r", "title")
        finally:
            os.environ.update(env)


class TestPromoteDraftIssue(unittest.TestCase):
    @patch("draft_issue.urllib.request.urlopen")
    def test_removes_draft_label(self, mock_urlopen):
        get_response = _make_response(
            {"number": 5, "labels": [{"name": "draft"}, {"name": "bug"}]}
        )
        patch_response = _make_response({"number": 5, "labels": [{"name": "bug"}]})
        mock_urlopen.side_effect = [get_response, patch_response]

        result = draft_issue.promote_draft_issue("o", "r", 5, token="tok")

        self.assertEqual(result["number"], 5)
        patch_call = mock_urlopen.call_args_list[1]
        req = patch_call[0][0]
        body = json.loads(req.data)
        self.assertNotIn("draft", body["labels"])
        self.assertIn("bug", body["labels"])


class TestListDraftIssues(unittest.TestCase):
    @patch("draft_issue.urllib.request.urlopen")
    def test_returns_draft_issues(self, mock_urlopen):
        issues = [
            {"number": 1, "title": "First draft"},
            {"number": 2, "title": "Second draft"},
        ]
        mock_urlopen.return_value = _make_response(issues)

        result = draft_issue.list_draft_issues("o", "r", token="tok")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "First draft")

    @patch("draft_issue.urllib.request.urlopen")
    def test_returns_empty_list(self, mock_urlopen):
        mock_urlopen.return_value = _make_response([])

        result = draft_issue.list_draft_issues("o", "r", token="tok")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
