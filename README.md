# main

## Web Application

`app.py` provides a small Flask web application with proper 404 error handling.

### Routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/items` | List all items |
| `GET` | `/items/<id>` | Get item by ID (404 if not found) |

Any unmatched route returns a JSON 404 response instead of the default HTML error page.

### Quick start

```bash
pip install flask
python app.py
```

### Running tests

```bash
pip install flask pytest
python -m pytest test_app.py -v
```