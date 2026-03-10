# main

A simple Python "Hello World" project.

## Requirements

- Python 3

## Usage

Run the script directly:

```bash
python hello.py
```

Expected output:

```
Hello, World!
```

Pass a name to greet someone specific:

```bash
python hello.py Alice
```

Expected output:

```
Hello, Alice!
```

## API

### `greet(name: str) -> str`

Returns a greeting string for the given name.

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | The name of the person to greet. |

**Returns**

A string in the form `Hello, <name>!`.

**Example**

```python
from hello import greet

print(greet("Alice"))   # Hello, Alice!
print(greet("World"))   # Hello, World!
```

## Project Structure

```
main/
├── .github/
│   └── copilot-instructions.md   # GitHub Copilot coding guidelines
├── hello.py                      # Main entry-point script and API
└── README.md                     # This file
```

## Contributing

1. Fork the repository and create a feature branch.
2. Follow the coding guidelines in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).
3. Open a pull request describing your changes.
