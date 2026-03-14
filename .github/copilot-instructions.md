# Copilot Instructions

## Tech Stack & Package Manager

- **Language**: Python 3
- **Package manager**: pip
- **Dependencies**: No external dependencies required

## Setup

Verify your environment is correctly configured:

```bash
python3 --version
```

Expected output: `Python 3.x.x`

## Running the Application

```bash
python3 hello.py
```

Expected output:

```
Hello World
```

## Testing

This project uses manual verification. Run the application and confirm the output:

```bash
python3 hello.py
```

Expected output: `Hello World`

## Linting

### Primary: flake8

Install and run:

```bash
pip install flake8
flake8 hello.py
```

### Alternative: pylint

Install and run:

```bash
pip install pylint
pylint hello.py
```

## Branch & PR Conventions

- **Branch naming**: Use the format `<type>/<short-description>` (e.g., `feature/add-greeting`, `fix/correct-output`, `chore/update-docs`)
- **Commit messages**: Use imperative mood (e.g., `Add greeting function`, `Fix output format`, `Update README`)
- **Pull requests**: Always open PRs against the `main` branch

## Configuration & Secrets

| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Copilot coding agent instructions |

### Environment Variables

No environment variables are required for this project.

### Secrets Handling

- Never commit secrets or credentials to the repository
- Use GitHub Actions secrets for any CI/CD sensitive values
- Reference secrets in workflows as `${{ secrets.SECRET_NAME }}`

### CI Placeholder

If adding CI/CD pipelines, place workflow files in `.github/workflows/`. For example, a basic Python lint workflow would live at `.github/workflows/lint.yml`.
