import imp
import os
from textwrap import dedent


def default_config_path():
    return os.path.expanduser(u'~/.chacractl')


def get_config_path():
    """
    Return the .chacractl configuration location
    """
    config = default_config_path()
    if os.path.exists(config):
        return config


def load_config():
    config = get_config_path()
    if not config:
        return
    return imp.load_source('chacractl', config)


def ensure_default_config():
    """
    Create a default config if the config file does not currently exist
    """
    template = dedent("""
    # This file was automatically generated by the chacractl CLI
    # make sure to update it with the correct user and key to talk to the API
    url = "http://example"
    user = "chacra user"
    key = "secret"
    """)
    config = default_config_path()
    if not os.path.exists(config):
        with open(config, 'w') as f:
            f.write(template)
