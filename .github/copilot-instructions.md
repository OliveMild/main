# Copilot Coding Agent Instructions

## Repository Overview

This is a Python project. The primary entry point is `hello.py`.

## Language & Tooling

- **Language**: Python 3
- **Linter**: [flake8](https://flake8.pycqa.org/) – enforces PEP 8 style
- **Formatter**: [black](https://black.readthedocs.io/) – opinionated code formatter
- **Tests**: [pytest](https://docs.pytest.org/)

## Running Tests Locally

```bash
# Install dev dependencies
pip install pytest flake8 black

# Run tests
pytest

# Run linter
flake8 .

# Check formatting
black --check .
```

## Running Tests in CI

CI is triggered automatically on every pull request. Tests and linting are run via the same commands listed above.

## Branch & PR Expectations

- Branch names should follow the pattern: `<type>/<short-description>` (e.g., `feat/add-greeting`, `fix/typo-in-readme`).
- Open a pull request against the `main` branch.
- Each PR should address a single concern and include a clear description.
- All CI checks must pass before merging.
- Link related issues in the PR description using `Closes #<issue-number>` or `Fixes #<issue-number>`.

## Code Conventions

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use `black` for automatic formatting before committing.
- Keep functions small and focused.
- Add docstrings to public functions and modules.
