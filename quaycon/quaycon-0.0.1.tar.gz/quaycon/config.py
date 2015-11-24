import logging
import os
import os.path as osp

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:  # pragma: no cover
    from yaml import Loader, Dumper
from six import string_types


LOGGER = logging.getLogger(__name__)
#: default configuration file locations.
DEFAULT_CONFIG_FILES = list(map(
    osp.expanduser,
    [
        "~/.quaycon.yml",
        "~/.config/quaycon/config.yml",
    ])
)


def load_config(path=None):
    """ quaycon YAML configuration loader.

    :param path:
      Load from a path or an opened file-like object.
      If kept to `None` then try loading configuration from HOME directory.

    :return: quaycon configuration
    :rtype: dict
    """
    if path is None:
        for path in DEFAULT_CONFIG_FILES:
            if osp.exists(path):
                logging.debug("Found config: %s", path)
                break
            else:
                logging.debug("Config does not exists: %s", path)
    if isinstance(path, string_types):
        if not osp.exists(path):
            return {}
        with open(path) as istr:
            return yaml.load(istr, Loader=Loader)
    return yaml.load(path, Loader=Loader)


def save_config(config, path=None):
    """ Save given quaycon configuration to YAML file

    :param dict config:
      configuration to save

    :param path:
      where to save the configuration. Can be either a path to a file, or
      an opened file-like object. If kept to `None`, then configuration is
      saved to ~/.quaycon.yml if it already exist or
      ~/.config/quaycon/config.yml
    """
    if path is None:
        for _path in DEFAULT_CONFIG_FILES:
            if osp.exists(_path):
                path = _path
                break
    if path is None:
        path = _path
    if isinstance(path, string_types):
        parent = osp.dirname(path)
        if not osp.isdir(parent):
            os.makedirs(parent)
        with open(path, 'w') as ostr:
            yaml.dump(config, ostr, encoding='utf-8',
                      default_flow_style=False, Dumper=Dumper)
    else:
        yaml.dump(config, path, encoding='utf-8',
                  default_flow_style=False, Dumper=Dumper)
