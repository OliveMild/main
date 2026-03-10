# main

A simple Hello World web application in Python.

## Usage

### Run as a web server

```bash
python hello.py
```

The server starts on port 8000. Visit `http://localhost:8000/` to see the greeting.

Any other path (e.g. `http://localhost:8000/unknown`) returns a `404 Not Found` response.

### Print a greeting directly

```bash
# Default greeting
python hello.py greet

# Greeting with a name
python hello.py greet Alice
```
