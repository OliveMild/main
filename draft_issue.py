#!/usr/bin/env python3
"""Create a GitHub issue via the REST API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def create_issue(owner, repo, title, body, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload = json.dumps({"title": title, "body": body}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
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
            print(f"Issue created: {result['html_url']}")
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        print(f"Error {exc.code}: {body_text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Draft a GitHub issue from the command line."
    )
    parser.add_argument("owner", help="GitHub organization or user name")
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
        parser.error(
            "A GitHub token is required. "
            "Pass --token or set the GITHUB_TOKEN environment variable."
        )

    create_issue(args.owner, args.repo, args.title, args.body, token)


if __name__ == "__main__":
    main()
