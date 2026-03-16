#!/usr/bin/env python3
"""Create a GitHub issue via the REST API.

Usage:
    # Use GITHUB_TOKEN environment variable
    export GITHUB_TOKEN=ghp_...
    python3 draft_issue.py myorg myrepo "Issue title" --body "Description"

    # Pass token inline
    python3 draft_issue.py myorg myrepo "Issue title" --token ghp_...
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = json.dumps({"title": title, "body": body}).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue using the GitHub REST API."
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
        print(
            "Error: a GitHub token is required. "
            "Set the GITHUB_TOKEN environment variable or use --token.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        issue = create_issue(args.owner, args.repo, args.title, args.body, token)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        print(f"Error {exc.code}: {exc.reason}\n{body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Unexpected API response (malformed JSON): {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        html_url = issue["html_url"]
    except KeyError as exc:
        print(f"Unexpected API response (missing field {exc})", file=sys.stderr)
        sys.exit(1)

    print(f"Issue created: {html_url}")


if __name__ == "__main__":
    main()
