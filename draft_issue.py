#!/usr/bin/env python3
"""Manage draft GitHub issues using a 'draft' label.

Usage:
  python draft_issue.py create  <org> <repo> <title>
  python draft_issue.py list    <org> <repo>
  python draft_issue.py promote <org> <repo> <issue_number>

Authentication:
  Set the GITHUB_TOKEN environment variable to a personal access token
  that has 'repo' scope for the target repository.
"""

import os
import sys

import requests

GITHUB_API = "https://api.github.com"
DRAFT_LABEL = "draft"


def _build_headers():
    token = os.environ.get("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _ensure_draft_label(org, repo):
    """Create the 'draft' label in the repo if it does not already exist."""
    url = f"{GITHUB_API}/repos/{org}/{repo}/labels/{DRAFT_LABEL}"
    if requests.get(url, headers=_build_headers()).status_code == 404:
        r = requests.post(
            f"{GITHUB_API}/repos/{org}/{repo}/labels",
            json={"name": DRAFT_LABEL, "color": "d3d3d3", "description": "Work in progress"},
            headers=_build_headers(),
        )
        r.raise_for_status()


def create_draft(org, repo, title):
    """Create a new issue and mark it as a draft."""
    _ensure_draft_label(org, repo)
    r = requests.post(
        f"{GITHUB_API}/repos/{org}/{repo}/issues",
        json={"title": title, "labels": [DRAFT_LABEL]},
        headers=_build_headers(),
    )
    r.raise_for_status()
    issue = r.json()
    print(f"Created draft issue #{issue['number']}: {issue['title']}")


def list_drafts(org, repo):
    """List all open draft issues."""
    r = requests.get(
        f"{GITHUB_API}/repos/{org}/{repo}/issues",
        params={"labels": DRAFT_LABEL, "state": "open"},
        headers=_build_headers(),
    )
    r.raise_for_status()
    issues = r.json()
    if not issues:
        print("No draft issues found.")
    else:
        for issue in issues:
            print(f"#{issue['number']}: {issue['title']}")


def promote_draft(org, repo, issue_number):
    """Promote a draft issue by removing the 'draft' label."""
    r = requests.delete(
        f"{GITHUB_API}/repos/{org}/{repo}/issues/{issue_number}/labels/{DRAFT_LABEL}",
        headers=_build_headers(),
    )
    if r.status_code == 404:
        print(f"Issue #{issue_number} does not have the '{DRAFT_LABEL}' label or does not exist.")
        sys.exit(1)
    r.raise_for_status()
    print(f"Promoted issue #{issue_number}: '{DRAFT_LABEL}' label removed.")


def main():
    if len(sys.argv) < 4:
        print("Error: insufficient arguments.\n")
        print(__doc__)
        sys.exit(1)

    command, org, repo = sys.argv[1], sys.argv[2], sys.argv[3]

    if command == "create":
        if len(sys.argv) < 5:
            print("Usage: python draft_issue.py create <org> <repo> <title>")
            sys.exit(1)
        create_draft(org, repo, sys.argv[4])

    elif command == "list":
        list_drafts(org, repo)

    elif command == "promote":
        if len(sys.argv) < 5:
            print("Usage: python draft_issue.py promote <org> <repo> <issue_number>")
            sys.exit(1)
        try:
            issue_number = int(sys.argv[4])
        except ValueError:
            print(f"Error: issue_number must be an integer, got '{sys.argv[4]}'")
            sys.exit(1)
        promote_draft(org, repo, issue_number)

    else:
        print(f"Unknown command: '{command}'")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
