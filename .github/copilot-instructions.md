# GitHub Copilot Instructions

## Project Overview

This is a Python project that serves as a simple "Hello World" application.

## Coding Guidelines

### Language & Style
- Use Python 3
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Keep lines under 79 characters where practical

### File Structure
- Entry-point scripts should include the `if __name__ == "__main__":` guard
- Use `#!/usr/bin/env python3` shebangs for executable scripts

### Naming Conventions
- `snake_case` for variables and functions
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants

### Documentation
- Write clear docstrings for all public functions, classes, and modules
- Keep comments concise and focused on *why*, not *what*

### Testing
- Place tests in a `tests/` directory
- Name test files `test_<module>.py`
- Use `pytest` as the test framework

### Dependencies
- List runtime dependencies in `requirements.txt`
- List development/test dependencies in `requirements-dev.txt`
