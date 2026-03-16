#!/usr/bin/env python3
"""Create a GitHub issue via the REST API.

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
import re
import sys
import urllib.request
import urllib.error

_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def _validate_slug(value: str, name: str) -> None:
    """Raise ValueError if *value* contains characters unsafe for a URL segment."""
    if not _SLUG_RE.match(value):
        raise ValueError(
            f"Invalid {name} {value!r}: only letters, digits, hyphens, "
            "underscores, and dots are allowed."
        )


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    """Create a GitHub issue and return the API response as a dict."""
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
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("owner", help="Repository owner (user or org)")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
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
            "Supply --token or set the GITHUB_TOKEN environment variable."
        )

    try:
        _validate_slug(args.owner, "owner")
        _validate_slug(args.repo, "repo")
    except ValueError as exc:
        parser.error(str(exc))

    try:
        issue = create_issue(args.owner, args.repo, args.title, args.body, token)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode(errors="replace")
        print(f"Error {exc.code}: {exc.reason}\n{err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)

    url = issue.get("html_url") or f"https://github.com/{args.owner}/{args.repo}/issues"
    print(f"Issue created: {url}")


if __name__ == "__main__":
    main()
