# main

A minimal Python repository.

## Modules

### `hello.py`

Prints (and returns) a greeting message.

#### Usage

Run directly:

```bash
python hello.py
```

Expected output:

```
Hello World
```

#### API

```python
from hello import greet

message = greet()
print(message)  # Hello World
```

**`greet() -> str`**  
Returns the greeting string `"Hello World"`.
