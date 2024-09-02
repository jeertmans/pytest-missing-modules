# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import date

from pytest_missing_modules.__version__ import __version__

project = "pytest_missing_modules"

if (year := date.today().year) != "2024":
    copyright = f"2024-{year}, Jérome Eertmans"
else:
    copyright = "2024, Jérome Eertmans"
author = "Jérome Eertmans"
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Built-in
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # Additional
    "myst_parser",
    "sphinxext.opengraph",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_remove_toctrees",
]

templates_path = []
exclude_patterns = []

add_module_names = False
add_function_parentheses = False

# -- Intersphinx mapping

intersphinx_mapping = {
    "pytest": ("https://docs.pytest.org/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
}

# -- OpenGraph settings

ogp_site_url = "https://eertmans.be/pytest-missing-modules/"
ogp_use_first_image = True

# -- Sphinx autodoc typehints settings

always_document_param_types = True

# -- MyST-nb settings

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = []

html_theme_options = {
    "show_toc_level": 2,
    "repository_url": "https://github.com/jeertmans/pytest-missing-modules",
    "repository_branch": "main",
    "path_to_docs": "docs/source",
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "navigation_with_keys": False,
}

autosummary_generate = True
napolean_use_rtype = False
