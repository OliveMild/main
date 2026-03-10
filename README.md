# main

A simple Python project demonstrating a Hello World application.

## Usage

Run the script with no arguments to print the default greeting:

```bash
python hello.py
```

Output:

```
Hello World
```

Pass a name to greet a specific person:

```bash
python hello.py Alice
```

Output:

```
Hello Alice
```

## API

### `greet(name="World")`

Returns a greeting string for the given name.

```python
from hello import greet

print(greet())         # Hello World
print(greet("Alice"))  # Hello Alice
```
