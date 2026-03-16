#!/usr/bin/env python3
"""Create a GitHub issue via the GitHub REST API."""

import argparse
import os
import sys
import urllib.request
import urllib.error
import json


def create_draft_issue(owner, repo, title, body="", token=None):
    """Create an issue in the specified GitHub repository."""
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GitHub token required. Use --token or set GITHUB_TOKEN.", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    data = json.dumps({"title": title, "body": body}).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Draft issue created: {result['html_url']}")
            return result
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode()
        print(f"Error {exc.code}: {body_text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create a GitHub issue.")
    parser.add_argument("owner", help="Repository owner (user or org)")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
    parser.add_argument("--token", default=None, help="GitHub personal access token")
    args = parser.parse_args()

    create_draft_issue(args.owner, args.repo, args.title, body=args.body, token=args.token)


if __name__ == "__main__":
    main()
