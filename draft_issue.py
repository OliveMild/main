#!/usr/bin/env python3
"""Create a GitHub issue via the GitHub REST API.

Usage:
    # via environment variable
    export GITHUB_TOKEN=ghp_...
    python draft_issue.py myorg myrepo "Issue title" --body "Description"

    # via inline token
    python draft_issue.py myorg myrepo "Issue title" --token ghp_...
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    """Create a GitHub issue and return the API response as a dict."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = json.dumps({"title": title, "body": body}).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode()
        sys.exit(f"GitHub API error {exc.code}: {error_body}")


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
        help="GitHub personal access token (falls back to GITHUB_TOKEN env var)",
    )

    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit(
            "Error: no GitHub token provided. "
            "Use --token or set the GITHUB_TOKEN environment variable."
        )

    issue = create_issue(args.owner, args.repo, args.title, args.body, token)
    html_url = issue.get("html_url")
    if html_url:
        print(f"Issue created: {html_url}")
    else:
        print(f"Issue created: #{issue.get('number', '?')} in {args.owner}/{args.repo}")


if __name__ == "__main__":
    main()
