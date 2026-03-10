# main

A minimal Python project that demonstrates a simple greeting API.

## Usage

Run the script directly:

```bash
python hello.py          # Hello, World!
python hello.py Alice    # Hello, Alice!
```

## API Reference

### `greet(name: str) -> str`

Return a greeting string for the given name.

| Parameter | Type  | Description        |
|-----------|-------|--------------------|
| `name`    | `str` | The name to greet. |

**Returns:** A greeting string of the form `"Hello, <name>!"`.

**Example:**

```python
from hello import greet

greet("Alice")  # "Hello, Alice!"
greet("World")  # "Hello, World!"
```