# Copilot Instructions

## Repository Overview

This is a simple Python "Hello World" repository.

## Language & Tooling

- **Primary language**: Python 3
- **No external dependencies** – the project uses only the Python standard library.

## Local Development

### Running the application

```bash
python3 hello.py
```

Expected output:

```
Hello World
```

### Install

No installation steps required. Python 3 must be available on the system.

### Tests

There is no test suite in this repository. When adding tests, use the `unittest` module from the Python standard library and place test files alongside the source (e.g. `test_hello.py`).

### Lint / Format

There is no linter or formatter configured. Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions when writing Python code.

## Conventions

- Keep `hello.py` as the entry point with an `if __name__ == "__main__":` guard.
- All Python files should begin with the `#!/usr/bin/env python3` shebang line.
- Prefer clear, readable code over brevity.

## Branch & PR Expectations

- Open a pull request for every change; do not commit directly to `main`.
- PR titles should be short and descriptive.
- Keep each PR focused on a single concern.
