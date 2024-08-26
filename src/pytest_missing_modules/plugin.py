import builtins
import importlib
import sys
from contextlib import AbstractContextManager as ContextManager
from contextlib import contextmanager
from threading import Lock
from types import ModuleType
from typing import Any, Protocol

import pytest


class MissingModulesContextGenerator(Protocol):
    def __call__(self, *names: str) -> ContextManager[pytest.MonkeyPatch]: ...


_LOCK = Lock()


@pytest.fixture
def missing_modules(monkeypatch: pytest.MonkeyPatch) -> MissingModulesContextGenerator:
    """Pytest fixture that can be used to create missing_modules contexts.

    Args:
    ----
        monkeypatch: A monkeypatch fixture, provided by :mod:`pytest`.

    """

    @contextmanager
    def ctx(
        *names: str, error_msg: str = "Mocked import error for '{name}'"
    ) -> ContextManager[pytest.MonkeyPatch]:
        """Context manager that mocks ImportError for a series of modules.

        In the provided context, an import of any modules in that list
        will raise an :py:class:`ImportError`.

        Args:
        ----
            names: A list of modules names.
            error_msg: A string template for import errors.

        """
        real_import = builtins.__import__
        real_import_module = importlib.import_module

        def monkey_import(name: str, *args: Any, **kwargs: Any) -> ModuleType:
            if name.partition(".")[0] in names:
                msg = error_msg.format(name=name)
                raise ImportError(msg)
            return real_import(name, *args, **kwargs)

        def monkey_import_module(name: str, *args: Any, **kwargs: Any) -> ModuleType:
            if name.partition(".")[0] in names:
                msg = error_msg.format(name=name)
                raise ImportError(msg)
            return real_import_module(name, *args, **kwargs)

        with monkeypatch.context() as m, _LOCK:
            module_names = tuple(sys.modules.keys())

            for module_name in module_names:
                if module_name.partition(".")[0] in names:
                    m.delitem(sys.modules, module_name)

            m.setattr(builtins, "__import__", monkey_import)
            m.setattr(importlib, "import_module", monkey_import_module)

            yield m  # type: ignore

    return ctx
