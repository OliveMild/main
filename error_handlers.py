class NotFoundError(Exception):
    code = 404

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def safe_call(func, *args, **kwargs):
    """Call *func* with the given arguments.

    Returns a ``(result, None)`` tuple on success, or
    ``(None, {"error": <message>, "code": <code>})`` when a
    :class:`NotFoundError` is raised.  All other exceptions propagate normally.
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except NotFoundError as e:
        return None, {"error": e.message, "code": e.code}
