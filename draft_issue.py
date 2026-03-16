#!/usr/bin/env python3
"""Create a GitHub issue via the GitHub REST API."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    """Create a GitHub issue and return the response JSON."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = {"title": title, "body": body}
    data = json.dumps(payload).encode()

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode()
        try:
            message = json.loads(error_body).get("message", error_body)
        except json.JSONDecodeError:
            message = error_body
        print(f"Error {exc.code}: {exc.reason} — {message}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue from the command line."
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
        print(
            "Error: no GitHub token provided. "
            "Use --token or set the GITHUB_TOKEN environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = create_issue(args.owner, args.repo, args.title, args.body, token)
    url = result.get("html_url")
    if url:
        print(f"Issue created: {url}")
    else:
        print(f"Issue created: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
