# pytest-missing-modules

Minimalist Pytest plugin that adds a fixture to fake missing modules.

## Who should use this plugin

Sometimes, your code needs to handle to possibility that
an optional dependency can be *missing*, e.g., a plotting
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


def test_missing_numpy(missing_modules):
    with missing_modules("numpy"):
        # Check that you can still import your package, without NumPy!
        importlib.reload("my_package")
```

If you need, you can also add type hints to your code:

```python
from pytest_missing_modules.plugin import MissingModulesContextGenerator


def test_missing_package(missing_modules: MissingModulesContextGenerator):
    # your test logic goes here
```
