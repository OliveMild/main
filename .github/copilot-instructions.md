# Copilot Instructions

## Repository Overview

This is a simple Python repository. The main entry point is `hello.py`.

## Tech Stack & Package Manager

- **Language**: Python 3
- **Package manager**: pip (standard library only; no `requirements.txt` at
  this time)
- **Entry point**: `hello.py`

## Project Structure

```
./
├── .github/
│   └── copilot-instructions.md
├── hello.py        # Main Python script
└── README.md       # Project documentation
```

## Setup

```bash
# No external dependencies — nothing to install beyond Python 3.
python3 --version   # verify Python 3 is available
```

## Running the Code

```bash
python3 hello.py
```

## Testing

There is no dedicated test suite at this time. Manually verify `hello.py`
runs without errors:

```bash
python3 hello.py   # expected output: Hello World
```

## Linting

Use `flake8` to lint Python files (PEP 8 compliance):

```bash
pip install flake8
flake8 hello.py
```

Alternatively, use `pylint`:

```bash
pip install pylint
pylint hello.py
```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use 4 spaces for indentation (no tabs).
- Keep lines under 79 characters.
- Use descriptive variable and function names.
- All Python files must start with the `#!/usr/bin/env python3` shebang line.

## Branch & PR Conventions

- Branch names: `<type>/<short-description>`, e.g. `feat/add-greeting`,
  `fix/typo-in-readme`, `docs/update-instructions`.
- Commit messages: use the imperative mood, e.g. `Add greeting function`,
  `Fix off-by-one error`.
- Keep commits small and focused; one logical change per commit.
- Open a pull request against `main`; include a brief description of what
  changed and why.

## Configuration Files

| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Coding-agent instructions (this file) |

- **CI**: No CI workflow is configured yet. Add workflows under `.github/workflows/`.
- **Environment variables**: None required.
- **Secrets**: Do not commit secrets or credentials. Use GitHub Actions
  secrets (Settings → Secrets and variables → Actions) if CI ever needs
  sensitive values.
