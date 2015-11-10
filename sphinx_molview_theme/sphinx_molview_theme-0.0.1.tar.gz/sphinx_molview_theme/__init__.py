"""Sphinx theme for MolView"""
import os
import sphinx_bootstrap_theme

VERSION = (0, 0, 1)

__version__ = ".".join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    return [
        sphinx_bootstrap_theme.get_html_theme_path()[0],
        cur_dir
    ]

def get_html_favicon_path():
    return 'favicon.ico'
