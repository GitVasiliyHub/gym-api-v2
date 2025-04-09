
from inspect import signature
from typing import Callable


def find_session(func: Callable) -> int:
    """Find session index in function call parameter."""
    func_params = signature(func).parameters
    try:
        session_args = tuple(func_params).index("session")
    except ValueError:
        raise ValueError(
            f"Function {func.__qualname__} has no session argument"
        ) from None

    return session_args