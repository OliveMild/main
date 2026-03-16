#!/usr/bin/env python3
"""Draft Issue Manager - create and manage GitHub draft issues."""

import json
import os
import urllib.error
import urllib.request


def _github_request(method, path, token, data=None):
    """Make an authenticated request to the GitHub REST API."""
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def create_draft_issue(owner, repo, title, body="", token=None):
    """Create a new issue in draft state.

    GitHub issues do not have a native "draft" state, so this function
    marks the issue with a ``draft`` label (creating it if needed) so
    it can be filtered and promoted later.

    Args:
        owner: Repository owner (user or organization).
        repo: Repository name.
        title: Issue title.
        body: Issue body (optional).
        token: GitHub personal-access token.  Falls back to the
            ``GITHUB_TOKEN`` environment variable when not supplied.

    Returns:
        The newly created issue as a dict.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("A GitHub token is required (pass token= or set GITHUB_TOKEN).")

    _ensure_draft_label(owner, repo, token)

    payload = {
        "title": title,
        "body": body,
        "labels": ["draft"],
    }
    return _github_request("POST", f"/repos/{owner}/{repo}/issues", token, payload)


def promote_draft_issue(owner, repo, issue_number, token=None):
    """Remove the ``draft`` label from an issue, promoting it to active.

    Args:
        owner: Repository owner.
        repo: Repository name.
        issue_number: Number of the issue to promote.
        token: GitHub personal-access token.

    Returns:
        The updated issue as a dict.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("A GitHub token is required (pass token= or set GITHUB_TOKEN).")

    issue = _github_request("GET", f"/repos/{owner}/{repo}/issues/{issue_number}", token)
    labels = [lbl["name"] for lbl in issue.get("labels", []) if lbl["name"] != "draft"]
    return _github_request(
        "PATCH",
        f"/repos/{owner}/{repo}/issues/{issue_number}",
        token,
        {"labels": labels},
    )


def list_draft_issues(owner, repo, token=None):
    """Return all open issues that carry the ``draft`` label.

    Args:
        owner: Repository owner.
        repo: Repository name.
        token: GitHub personal-access token.

    Returns:
        List of issue dicts.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("A GitHub token is required (pass token= or set GITHUB_TOKEN).")

    path = f"/repos/{owner}/{repo}/issues?labels=draft&state=open&per_page=100"
    return _github_request("GET", path, token)


def _ensure_draft_label(owner, repo, token):
    """Create the ``draft`` label in the repo if it doesn't exist yet."""
    try:
        _github_request("GET", f"/repos/{owner}/{repo}/labels/draft", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        _github_request(
            "POST",
            f"/repos/{owner}/{repo}/labels",
            token,
            {"name": "draft", "color": "d3d3d3", "description": "Work in progress / draft"},
        )


if __name__ == "__main__":
    import sys

    def _usage():
        print(
            "Usage:\n"
            "  draft_issue.py create  <owner> <repo> <title> [body]\n"
            "  draft_issue.py list    <owner> <repo>\n"
            "  draft_issue.py promote <owner> <repo> <issue_number>\n"
        )
        sys.exit(1)

    if len(sys.argv) < 4:
        _usage()

    cmd = sys.argv[1]
    owner_arg = sys.argv[2]
    repo_arg = sys.argv[3]

    if cmd == "create":
        if len(sys.argv) < 5:
            _usage()
        title_arg = sys.argv[4]
        body_arg = sys.argv[5] if len(sys.argv) > 5 else ""
        issue = create_draft_issue(owner_arg, repo_arg, title_arg, body_arg)
        print(f"Created draft issue #{issue['number']}: {issue['html_url']}")

    elif cmd == "list":
        issues = list_draft_issues(owner_arg, repo_arg)
        if not issues:
            print("No open draft issues.")
        for i in issues:
            print(f"  #{i['number']} {i['title']}")

    elif cmd == "promote":
        if len(sys.argv) < 5:
            _usage()
        number_arg = int(sys.argv[4])
        issue = promote_draft_issue(owner_arg, repo_arg, number_arg)
        print(f"Promoted issue #{issue['number']} to active.")

    else:
        _usage()
