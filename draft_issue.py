#!/usr/bin/env python3
"""Create a GitHub issue via the GitHub REST API."""

import argparse
import json
import os
import urllib.error
import urllib.request


def create_draft_issue(owner, repo, title, body="", token=None):
    """Create an issue in a GitHub repository.

    Args:
        owner: Repository owner (user or organization).
        repo: Repository name.
        title: Issue title.
        body: Issue body text (optional).
        token: GitHub personal access token. Falls back to GITHUB_TOKEN env var.

    Returns:
        dict: The created issue data from the GitHub API.

    Raises:
        ValueError: If no token is provided or found in environment.
        urllib.error.HTTPError: If the API request fails.
    """
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "A GitHub token is required. Set GITHUB_TOKEN or pass --token."
        )

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = json.dumps({"title": title, "body": body}).encode()

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue via the GitHub API."
    )
    parser.add_argument("owner", help="Repository owner (user or organization)")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub personal access token (defaults to GITHUB_TOKEN env var)",
    )
    args = parser.parse_args()

    try:
        issue = create_draft_issue(args.owner, args.repo, args.title, args.body, args.token)
        print(f"Issue created: {issue['html_url']}")
    except ValueError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error {exc.code}: {exc.read().decode()}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
