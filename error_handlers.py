class NotFoundError(Exception):
    code = 404


def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), None
    except NotFoundError as e:
        return None, {"error": str(e), "code": e.code}
