from __future__ import annotations

import importlib
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
def test_missing_modules_one_module(
    names: tuple[str, ...],
    missing_modules: MissingModulesContextGenerator,
) -> None:
    for name in names:
        importlib.import_module(name)

    with missing_modules(*names):
        for name in names:
            with pytest.raises(ImportError, match="Mocked"):
                importlib.import_module(name)

    for name in names:
        importlib.import_module(name)
