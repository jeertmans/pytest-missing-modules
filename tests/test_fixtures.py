from __future__ import annotations

import importlib
import importlib.util
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_missing_modules.plugin import MissingModulesContextGenerator


@pytest.mark.parametrize(
    "names",
    [
        ("os",),
        (
            "os",
            "pathlib",
        ),
    ],
)
def test_missing_modules(
    names: tuple[str, ...],
    missing_modules: MissingModulesContextGenerator,
) -> None:
    for name in names:
        importlib.import_module(name)

    with missing_modules(*names):
        for name in names:
            with pytest.raises(ImportError):
                importlib.import_module(name)

    for name in names:
        importlib.import_module(name)


def test_missing_modules_submodules(
    missing_modules: MissingModulesContextGenerator,
) -> None:
    with missing_modules("os"):
        for name in ("os", "os.path"):
            with pytest.raises(
                ImportError,
            ):
                importlib.import_module(name)


@pytest.mark.parametrize(
    "names",
    [
        ("os",),
        (
            "os",
            "pathlib",
        ),
    ],
)
def test_missing_modules_custom_error_msg(
    names: tuple[str, ...],
    missing_modules: MissingModulesContextGenerator,
) -> None:
    with missing_modules(*names):
        for name in names:
            with pytest.raises(ImportError, match=f"Mocked import error for '{name}'"):
                importlib.import_module(name)

    with missing_modules(*names, error_msg="My custom error message for '{name}'"):  # noqa: RUF027
        for name in names:
            with pytest.raises(
                ImportError,
            ):
                importlib.import_module(name)


@pytest.mark.parametrize(
    "names",
    [
        ("os",),
        (
            "os",
            "pathlib",
        ),
    ],
)
@pytest.mark.parametrize(
    ("patch_import", "expectation"),
    [(True, pytest.raises(ImportError)), (False, does_not_raise())],
)
def test_missing_modules_patch_import(
    names: tuple[str, ...],
    patch_import: bool,
    expectation: AbstractContextManager[Exception],
    missing_modules: MissingModulesContextGenerator,
) -> None:
    with missing_modules(*names, patch_import=patch_import):
        for name in names:
            with expectation:
                importlib.import_module(name)


@pytest.mark.parametrize(
    "names",
    [
        ("os",),
        (
            "os",
            "pathlib",
        ),
    ],
)
@pytest.mark.parametrize("patch_find_spec", [True, False])
def test_missing_modules_patch_find_spec(
    names: tuple[str, ...],
    patch_find_spec: bool,
    missing_modules: MissingModulesContextGenerator,
) -> None:
    with missing_modules(*names, patch_find_spec=patch_find_spec):
        for name in names:
            if patch_find_spec:
                assert importlib.util.find_spec(name) is None
            else:
                assert importlib.util.find_spec(name) is not None
