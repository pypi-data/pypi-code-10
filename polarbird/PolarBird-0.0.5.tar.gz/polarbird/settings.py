import os
import json

class Settings(object):

    BASE_DIR = os.path.dirname(__file__)

    USER_DIR = os.getenv(
        'XDG_CONFIG_HOME', os.path.join(
            os.path.expanduser('~'), '.config', 'polarbird/'
        )
    )

    def __init__(self):
        default_config_path = os.path.join(
            Settings.BASE_DIR, 'config', 'config.json'
        )
        custom_config_path = os.path.join(Settings.USER_DIR, 'config.json')
        default_config = self._load_config(default_config_path)
        custom_config = self._load_config(custom_config_path)
        default_config.update(custom_config)

        self._config = default_config

    def _load_config(self, path):
        config = {}
        if os.path.exists(path):
            config_file = open(path)
            config = json.load(config_file)

        return config

    def __getattr__(self, name):
        return self._config[name]

settings = Settings()
