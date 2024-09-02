# pytest-missing-modules

[![Latest Release][pypi-version-badge]][pypi-version-url]
[![Python version][pypi-python-version-badge]][pypi-version-url]
[![Documentation][documentation-badge]][documentation-url]

Minimalist Pytest plugin that adds a fixture to fake missing modules.

## Who should use this plugin

Sometimes, your code needs to handle the possibility that
an optional dependency can be *missing*, e.g., you develop a plotting
library supporting multiple drawing backends.

This plugin provides a convenient way to simulate one
or multiple missing modules, raising an `ImportError` instead.

## Usage

First, install this plugin with:

```bash
pip install pytest-missing-modules
```

Then, you use the Pytest fixtures like so:

```python
# this should be in one of your test files
import importlib
import my_package


def test_missing_numpy(missing_modules):
    with missing_modules("numpy"):
        # Check that you can still import your package, without NumPy!
        importlib.reload(my_package)
```

If you need, you can also add type hints to your code:

```python
from pytest_missing_modules.plugin import MissingModulesContextGenerator


def test_missing_package(missing_modules: MissingModulesContextGenerator):
    # your test logic goes here
```

For more advance usage, please check the
[documentation](https://pytest-missing-modules.readthedocs.io/).

## Contributing

This project welcomes any contribution, and especially:

+ bug fixes;
+ or documentation typos.

[pypi-version-badge]: https://img.shields.io/pypi/v/pytest-missing-modules?label=pytest-missing-modules
[pypi-version-url]: https://pypi.org/project/pytest-missing-modules/
[pypi-python-version-badge]: https://img.shields.io/pypi/pyversions/pytest-missing-modules
[pypi-download-badge]: https://img.shields.io/pypi/dm/pytest-missing-modules
[documentation-badge]: https://readthedocs.org/projects/pytest-missing-modules/badge/?version=latest
[documentation-url]: https://pytest-missing-modules.readthedocs.io/
