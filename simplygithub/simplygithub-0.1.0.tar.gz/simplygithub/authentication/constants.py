# -*- coding: utf-8 -*-

"""Constants are defined here."""

import os


CONFIG_FOLDER = os.path.join(os.path.expanduser("~"), ".profile", "tabu")
"""The folder where config files are kept."""


CONFIG_FILE = os.path.join(CONFIG_FOLDER, "github") 
"""The path to the config file itself."""
