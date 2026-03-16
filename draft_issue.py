#!/usr/bin/env python3
"""Create GitHub draft issues via the GitHub REST API."""

import argparse
import json
import sys
import urllib.error
import urllib.request


def create_draft_issue(token: str, owner: str, repo: str, title: str, body: str = "") -> dict:
    """Create a draft issue in a GitHub repository.

    GitHub's REST API does not have a native "draft issue" concept, so this
    function creates an issue with the ``draft`` label applied at creation
    time.  The newly created issue data is returned as a dictionary.

    Args:
        token: A GitHub personal access token with ``repo`` scope.
        owner: The repository owner (user or organization).
        repo:  The repository name.
        title: The issue title.
        body:  Optional issue body / description.

    Returns:
        A dictionary containing the created issue data returned by the API.

    Raises:
        urllib.error.HTTPError: If the GitHub API returns an error status.
        ValueError: If required arguments are empty.
    """
    if not token:
        raise ValueError("token must not be empty")
    if not owner:
        raise ValueError("owner must not be empty")
    if not repo:
        raise ValueError("repo must not be empty")
    if not title:
        raise ValueError("title must not be empty")

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = json.dumps({"title": title, "body": body, "labels": ["draft"]}).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }

    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def main(argv: list[str] | None = None) -> int:
    """Entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Create a GitHub draft issue.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--title", required=True, help="Issue title")
    parser.add_argument("--body", default="", help="Issue body (optional)")

    args = parser.parse_args(argv)

    try:
        issue = create_draft_issue(
            token=args.token,
            owner=args.owner,
            repo=args.repo,
            title=args.title,
            body=args.body,
        )
    except urllib.error.HTTPError as exc:
        print(f"Error: GitHub API returned {exc.code}: {exc.reason}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Draft issue created: #{issue['number']} - {issue['html_url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
