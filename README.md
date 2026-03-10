# main

A simple Python project.

## Getting Started

### Prerequisites

- Python 3.x

### Running the application

```bash
python hello.py
```

**Output:**

```
Hello World
```

## API Reference

### `hello.py`

Entry point script. When executed directly it prints `Hello World` to standard output.

#### Usage as a script

```bash
python hello.py
```

#### Usage as a module

```python
import runpy
runpy.run_path("hello.py")  # prints "Hello World"
```

## Project Structure

```
main/
└── hello.py   # Entry point – prints "Hello World"
```