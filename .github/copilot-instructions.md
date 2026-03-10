# Copilot Coding Agent Instructions

## Language & Runtime

- Python 3.8+ only. No Python 2 compatibility required.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for all Python code.
- Use 4 spaces for indentation (no tabs).
- Maximum line length: 88 characters.
- Use `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_CASE` for constants.

## Docstrings

- All public functions, classes, and modules must have docstrings.
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings):
  ```python
  def greet(name: str) -> str:
      """Return a greeting string for the given name.

      Args:
          name: The name to greet.

      Returns:
          A greeting string of the form "Hello, <name>!".
      """
  ```

## Type Annotations

- Add type annotations to all function signatures.

## Testing

- Place tests in a `tests/` directory.
- Use `pytest` as the test runner: `pytest tests/`
- Name test files `test_<module>.py` and test functions `test_<behaviour>`.

## Dependencies

- List runtime dependencies in `requirements.txt`.
- List development/test dependencies in `requirements-dev.txt`.

## Git

- Commit messages should be concise and written in the imperative mood (e.g., "Add greet function").
- Keep PRs focused on a single concern.
