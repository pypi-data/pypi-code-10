# -*- coding: utf-8 -*-

"""Constants used by the ``authentication`` package."""

import os


CONFIG_FOLDER = os.path.join(
    os.path.expanduser("~"),
    ".profile",
    "simplygithub")
"""The folder where config files are kept."""


CONFIG_FILE = os.path.join(CONFIG_FOLDER, "github")
"""The path to the config file itself."""
