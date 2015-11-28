import os
import yaml

from amiorganizer.errors.Errors import AppConfigError


class AppConfig:
    """Loader and accessor for Application config file"""

    def __init__(self, app_config_path):
        self.app_config_path = app_config_path

        if not os.path.isfile(app_config_path) and os.access(app_config_path, os.R_OK):
            raise AppConfigError("Config not found or not readable at path: {}.".format(app_config_path))

        with open(app_config_path, 'r') as file:
            self.app_config = yaml.load(file)
