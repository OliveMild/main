"""Utilities for managing GitHub draft issues."""

import requests

GITHUB_API = "https://api.github.com"
DRAFT_LABEL = "draft"


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def create_draft_issue(org, repo, title, *, token):
    """Create a draft issue in a GitHub repository.

    The issue is created with a 'draft' label to indicate its draft status.

    Args:
        org: GitHub organization or user name.
        repo: Repository name.
        title: Title of the issue.
        token: GitHub personal access token.

    Returns:
        The created issue as a dict (includes 'number', 'title', etc.).

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API}/repos/{org}/{repo}/issues"
    payload = {"title": title, "labels": [DRAFT_LABEL]}
    response = requests.post(url, json=payload, headers=_headers(token))
    response.raise_for_status()
    return response.json()


def promote_draft_issue(org, repo, issue_number, *, token):
    """Promote a draft issue by removing its 'draft' label.

    Args:
        org: GitHub organization or user name.
        repo: Repository name.
        issue_number: The issue number to promote.
        token: GitHub personal access token.

    Returns:
        The updated issue as a dict.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API}/repos/{org}/{repo}/issues/{issue_number}"

    # Fetch current labels
    response = requests.get(url, headers=_headers(token))
    response.raise_for_status()
    issue = response.json()

    # Remove the draft label
    labels = [
        label["name"]
        for label in issue.get("labels", [])
        if label["name"] != DRAFT_LABEL
    ]

    # Patch the issue with updated labels
    response = requests.patch(url, json={"labels": labels}, headers=_headers(token))
    response.raise_for_status()
    return response.json()
