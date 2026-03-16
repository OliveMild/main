# main

## Draft Issue Manager

`draft_issue.py` provides a small CLI and importable module for managing **draft GitHub issues**.

GitHub issues don't have a built-in draft state, so this tool uses a `draft` label
(created automatically if it doesn't exist) to mark issues that are works-in-progress.

### Requirements

* Python 3.8+
* A GitHub personal-access token with `repo` scope exported as the
  `GITHUB_TOKEN` environment variable.

### Usage

```bash
export GITHUB_TOKEN=ghp_...

# Create a draft issue
python draft_issue.py create <owner> <repo> "My draft title" "Optional body"

# List all open draft issues
python draft_issue.py list <owner> <repo>

# Promote a draft to an active issue (removes the draft label)
python draft_issue.py promote <owner> <repo> <issue_number>
```

### API

```python
from draft_issue import create_draft_issue, list_draft_issues, promote_draft_issue

issue = create_draft_issue("owner", "repo", "Title", "Body", token="...")
drafts = list_draft_issues("owner", "repo", token="...")
active = promote_draft_issue("owner", "repo", issue["number"], token="...")
```

### Tests

```bash
python -m unittest test_draft_issue -v
```
