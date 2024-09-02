"""Pytest plugin implementation."""

from __future__ import annotations

import builtins
import importlib
import importlib.util
import sys
from contextlib import contextmanager
from functools import wraps
from threading import Lock
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import (
        Callable,
    )

    if sys.version_info >= (3, 10):
        from typing import Concatenate, ParamSpec, TypeVar
    else:
        from typing_extension import Concatenate, ParamSpec, TypeVar

    P = ParamSpec("P")
    R = TypeVar("R")


_LOCK = Lock()
"""Lock used to make sure that :func:`missing_modules` is compatible
with :mod:`pytest-xdist`."""


class MissingModulesContextGenerator:
    """Context manager generator that raises ImportError for a series of modules.

    In the provided context, an import of any modules in that list
    will raise an :py:class:`ImportError`.

    Args:
        monkeypatch: The monkeypatch object used to perform
            all patches.
    """

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: D107
        self.monkeypatch = monkeypatch

    @contextmanager
    def __call__(  # noqa: C901
        self,
        *names: str,
        error_msg: str = "Mocked import error for '{name}'",
        patch_import: bool = True,
        patch_find_spec: bool = True,
    ) -> Iterator[pytest.MonkeyPatch]:
        """Enter the context manager.

        Args:
            names: A list of modules names.
            error_msg: A string template for import errors.
            patch_import: Whether to patch :func:`import<__import__>` and
                :func:`importlib.import_module`.
            patch_find_spec: Whether to patch
                :func:`importlib.util.find_spec`.

        Yields:
            A monkeypatch instance that mocks imports of the specified
            modules.
        """
        real_import = builtins.__import__
        real_import_module = importlib.import_module
        real_find_spec = importlib.util.find_spec

        def should_mock(name: str) -> bool:
            return name.partition(".")[0] in names

        def mock_import_func(
            import_func: Callable[Concatenate[str, P], R],
        ) -> Callable[Concatenate[str, P], R]:
            @wraps(import_func)
            def wrapper(name: str, *args: P.args, **kwargs: P.kwargs) -> R:
                if should_mock(name):
                    msg = error_msg.format(name=name)
                    raise ImportError(msg)
                return import_func(name, *args, **kwargs)

            return wrapper

        def mock_find_spec_func(
            find_spec_func: Callable[Concatenate[str, P], R],
        ) -> Callable[Concatenate[str, P], R | None]:
            @wraps(find_spec_func)
            def wrapper(name: str, *args: P.args, **kwargs: P.kwargs) -> R | None:
                if should_mock(name):
                    return None
                return find_spec_func(name, *args, **kwargs)

            return wrapper

        with self.monkeypatch.context() as m, _LOCK:
            module_names = tuple(sys.modules.keys())

            for module_name in module_names:
                if module_name.partition(".")[0] in names:
                    m.delitem(sys.modules, module_name)

            if patch_import:
                m.setattr(builtins, "__import__", mock_import_func(real_import))
                m.setattr(
                    importlib,
                    "import_module",
                    mock_import_func(real_import_module),
                )

            if patch_find_spec:
                m.setattr(
                    importlib.util,
                    "find_spec",
                    mock_find_spec_func(real_find_spec),
                )

            yield m


@pytest.fixture
def missing_modules(monkeypatch: pytest.MonkeyPatch) -> MissingModulesContextGenerator:
    """Pytest fixture that can be used to create missing_modules contexts.

    Args:
        monkeypatch: A monkeypatch fixture, provided by :mod:`pytest`.

    Returns:
        A context manager that can be used to create missing modules contexts.

    Examples:
        This first examples shows the most basic usage of this module.

        .. code-block:: python
            :caption: The following must be placed in a test file.

            import pytest


            def test_missing_numpy(missing_modules):
                with missing_modules("numpy"):
                    with pytest.raises(ImportError):
                        # Will always raise an error, even if NumPy is installed
                        import numpy

        A more interesting example would be to check that your package can still
        be imported, even if a dependency is missing.

        .. code-block:: python
            :caption: The following must be placed in a test file.

            import importlib
            import importlib.util
            import pytest
            import my_package  # This succeeds


            def test_missing_dependency(missing_modules):
                with missing_modules("plotly", patch_find_spec=False):
                    # We check that Plotly is installed
                    assert importlib.util.find_spec("plotly") is not None
                    # .. but not importable
                    with pytest.raises(ImportError):
                        import plotly

                    # We check our package can still be imported
                    importlib.reload(my_package)
    """
    return MissingModulesContextGenerator(monkeypatch)
