"""Tests for draft_issue module."""

import unittest
from unittest.mock import MagicMock, patch, call

from draft_issue import create_draft_issue, promote_draft_issue


class TestCreateDraftIssue(unittest.TestCase):
    @patch("draft_issue.requests.post")
    def test_creates_issue_with_draft_label(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"number": 42, "title": "WIP: new feature"}
        mock_post.return_value = mock_response

        result = create_draft_issue("myorg", "myrepo", "WIP: new feature", token="tok")

        mock_post.assert_called_once_with(
            "https://api.github.com/repos/myorg/myrepo/issues",
            json={"title": "WIP: new feature", "labels": ["draft"]},
            headers={
                "Authorization": "Bearer tok",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result["number"], 42)

    @patch("draft_issue.requests.post")
    def test_raises_on_http_error(self, mock_post):
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("403")
        mock_post.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            create_draft_issue("org", "repo", "title", token="bad_token")


class TestPromoteDraftIssue(unittest.TestCase):
    @patch("draft_issue.requests.patch")
    @patch("draft_issue.requests.get")
    def test_removes_draft_label(self, mock_get, mock_patch):
        get_response = MagicMock()
        get_response.json.return_value = {
            "number": 42,
            "labels": [{"name": "draft"}, {"name": "bug"}],
        }
        mock_get.return_value = get_response

        patch_response = MagicMock()
        patch_response.json.return_value = {"number": 42, "labels": [{"name": "bug"}]}
        mock_patch.return_value = patch_response

        result = promote_draft_issue("myorg", "myrepo", 42, token="tok")

        expected_url = "https://api.github.com/repos/myorg/myrepo/issues/42"
        expected_headers = {
            "Authorization": "Bearer tok",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        mock_get.assert_called_once_with(expected_url, headers=expected_headers)
        mock_patch.assert_called_once_with(
            expected_url, json={"labels": ["bug"]}, headers=expected_headers
        )
        mock_patch.return_value.raise_for_status.assert_called_once()
        self.assertEqual(result["number"], 42)

    @patch("draft_issue.requests.patch")
    @patch("draft_issue.requests.get")
    def test_promotes_with_no_other_labels(self, mock_get, mock_patch):
        get_response = MagicMock()
        get_response.json.return_value = {
            "number": 7,
            "labels": [{"name": "draft"}],
        }
        mock_get.return_value = get_response

        patch_response = MagicMock()
        patch_response.json.return_value = {"number": 7, "labels": []}
        mock_patch.return_value = patch_response

        result = promote_draft_issue("org", "repo", 7, token="tok")

        mock_patch.assert_called_once_with(
            "https://api.github.com/repos/org/repo/issues/7",
            json={"labels": []},
            headers=unittest.mock.ANY,
        )
        self.assertEqual(result["number"], 7)

    @patch("draft_issue.requests.get")
    def test_raises_on_get_http_error(self, mock_get):
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            promote_draft_issue("org", "repo", 99, token="tok")


if __name__ == "__main__":
    unittest.main()
