# main

## draft_issue.py

Create a GitHub issue from the command line.

### Usage

```bash
# Using an environment variable
export GITHUB_TOKEN=ghp_...
python draft_issue.py myorg myrepo "Issue title" --body "Description"

# Passing the token inline
python draft_issue.py myorg myrepo "Issue title" --token ghp_...
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `owner`  | Yes | Repository owner (user or organization) |
| `repo`   | Yes | Repository name |
| `title`  | Yes | Issue title |
| `--body` | No  | Issue body / description |
| `--token`| No  | GitHub personal access token (falls back to `GITHUB_TOKEN` env var) |
