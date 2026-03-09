# Copilot Instructions

## Repository Overview

This is a minimal Python repository containing a single "Hello World" script. It serves as a simple starting point or template project.

- **Language:** Python 3
- **Type:** Simple script / template
- **Size:** Very small (1 source file)

## Project Layout

```
main/
├── .github/
│   └── copilot-instructions.md  # This file
├── hello.py                     # Main Python script (entry point)
└── README.md                    # Project readme
```

### Key Files

- `hello.py` — The main script. Contains a `__main__` guard and prints "Hello World" when executed.

## Running the Project

```bash
python3 hello.py
```

Expected output:
```
Hello World
```

## Build & Test

There is no build step. There are no automated tests or CI pipelines configured in this repository.

To validate a change:
1. Run `python3 hello.py` and confirm the output is as expected.
2. Optionally run `python3 -m py_compile hello.py` to syntax-check the file without executing it.

## Notes for the Coding Agent

- Trust the instructions above; no additional exploration is needed for this small repository.
- If you add new Python files, follow the existing style: use an `if __name__ == "__main__":` guard for executable scripts.
- There are no linting, formatting, or dependency management tools configured (no `requirements.txt`, `pyproject.toml`, `setup.py`, or `.flake8`). Keep changes minimal unless explicitly asked to add tooling.
