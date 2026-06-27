"""
Error handling and loading state utilities for frontend applications.
"""

from typing import Any, Optional, Callable
from enum import Enum


class LoadingState(str, Enum):
    """Loading states."""
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


class Loadable:
    """A wrapper for values that can be in different loading states."""

    def __init__(self, initial_value: Any = None):
        self._value = initial_value
        self._state = LoadingState.IDLE if initial_value is not None else LoadingState.IDLE
        self._error: Optional[Exception] = None

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val: Any) -> None:
        self._value = val
        self._state = LoadingState.SUCCESS
        self._error = None

    @property
    def state(self) -> LoadingState:
        return self._state

    def set_loading(self) -> None:
        self._state = LoadingState.LOADING
        self._error = None

    def set_error(self, error: Exception) -> None:
        self._state = LoadingState.ERROR
        self._error = error

    def reset(self) -> None:
        self._state = LoadingState.IDLE
        self._value = None
        self._error = None

    def is_loading(self) -> bool:
        return self._state == LoadingState.LOADING

    def is_success(self) -> bool:
        return self._state == LoadingState.SUCCESS

    def is_error(self) -> bool:
        return self._state == LoadingState.ERROR

    def get_error(self) -> Optional[Exception]:
        return self._error


def safe_execute(func: Callable, *args, **kwargs) -> Loadable:
    """Execute a function and wrap the result in a Loadable, capturing any exceptions."""
    result = Loadable()
    try:
        result.value = func(*args, **kwargs)
    except Exception as e:
        result.set_error(e)
    return result