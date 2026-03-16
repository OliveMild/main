#!/usr/bin/env python3
"""Create a GitHub issue via the REST API.

Usage:
    # Environment variable
    export GITHUB_TOKEN=ghp_...
    python draft_issue.py myorg myrepo "Issue title" --body "Description"

    # Inline token
    python draft_issue.py myorg myrepo "Issue title" --token ghp_...
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    """Create a GitHub issue and return the response as a dict."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = {"title": title, "body": body}
    data = json.dumps(payload).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="replace")
        try:
            message = json.loads(error_body).get("message", error_body)
        except json.JSONDecodeError:
            message = error_body
        print(f"Error {exc.code}: {message}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("owner", help="Repository owner (user or organization)")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body / description")
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub personal access token (overrides GITHUB_TOKEN env var)",
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        parser.error(
            "A GitHub token is required. "
            "Supply --token or set the GITHUB_TOKEN environment variable."
        )

    issue = create_issue(args.owner, args.repo, args.title, args.body, token)
    print(f"Issue created: {issue['html_url']}")


if __name__ == "__main__":
    main()
