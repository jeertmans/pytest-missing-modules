"""Pytest plugin implementation."""

from __future__ import annotations

import builtins
import importlib
import sys
from contextlib import AbstractContextManager, contextmanager
from functools import wraps
from threading import Lock
from typing import TYPE_CHECKING, Protocol

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import (
        Callable,
        Concatenate,
        ParamSpec,
        TypeVar,
    )

    P = ParamSpec("P")
    R = TypeVar("R")


class MissingModulesContextGenerator(Protocol):
    """Context manager that raises ImportError for a series of modules.

    In the provided context, an import of any modules in that list
    will raise an :py:class:`ImportError`.
    """

    def __call__(
        self, *names: str, error_msg: str = "Mocked import error for '{name}'"
    ) -> AbstractContextManager[pytest.MonkeyPatch]:
        """Enter the context manager.

        Args:
            names: A list of modules names.
            error_msg: A string template for import errors.

        Yields:
            A monkeypatch instance that mocks imports of the specified
            modules.
        """
        ...


_LOCK = Lock()
"""Lock used to make sure that :func:`missing_modules` is compatible
with :mod:`pytest-xdist`."""


@pytest.fixture
def missing_modules(monkeypatch: pytest.MonkeyPatch) -> MissingModulesContextGenerator:
    """Pytest fixture that can be used to create missing_modules contexts.

    Args:
        monkeypatch: A monkeypatch fixture, provided by: mod:`pytest`.

    Returns:
        A context manager that can be used to create missing_modules contexts.
    """

    @contextmanager
    def ctx(
        *names: str,
        error_msg: str = "Mocked import error for '{name}'",
    ) -> Iterator[pytest.MonkeyPatch]:
        real_import = builtins.__import__
        real_import_module = importlib.import_module

        def mock_import_func(
            import_func: Callable[Concatenate[str, P], R],
        ) -> Callable[Concatenate[str, P], R]:
            @wraps(import_func)
            def wrapper(name: str, *args: P.args, **kwargs: P.kwargs) -> R:
                if name.partition(".")[0] in names:
                    msg = error_msg.format(name=name)
                    raise ImportError(msg)
                return import_func(name, *args, **kwargs)

            return wrapper

        with monkeypatch.context() as m, _LOCK:
            module_names = tuple(sys.modules.keys())

            for module_name in module_names:
                if module_name.partition(".")[0] in names:
                    m.delitem(sys.modules, module_name)

            m.setattr(builtins, "__import__", mock_import_func(real_import))
            m.setattr(importlib, "import_module", mock_import_func(real_import_module))

            yield m

    return ctx
