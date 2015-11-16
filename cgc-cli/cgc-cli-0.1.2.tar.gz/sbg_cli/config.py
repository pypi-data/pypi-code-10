__author__ = 'Sinisa'

import os
import json
import logging


DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), '.sbgenomics.conf')

DEFAULT_DOCKER_API_VERSION = '1.17'
DEFAULT_DOCKER_CLIENT_TIMEOUT = 240
DEFAULT_DOCKER_REGISTRY_URL = "images.sbgenomics.com"
DEFAULT_AUTH_SERVER_URL = "https://hatchery.sbgenomics.com"
DEFAULT_APP_REGISTRY_URL = "brood.sbgenomics.com"
DEFAULT_PLATFORM_URL = ("www.sbgenomics.com", 'igor.sbgenomics.com')
DEFAULT_DOCKER_HUB = "index.docker.io"
DEFAULT_LOG_LEVEL = logging.FATAL


CGC_DOCKER_REGISTRY_URL = "cgc-images.sbgenomics.com"
CGC_AUTH_SERVER_URL = "https://cgc-hatchery.sbgenomics.com"
CGC_GK_AUTH_SERVER_URL = "https://cgc-gatekeeper.sbgenomics.com"
CGC_APP_REGISTRY_URL = "cgc-brood.sbgenomics.com"
CGC_PLATFORM_URL = ("cgc.sbgenomics.com", 'cgc-igor.sbgenomics.com')


DEFAULT_CONFIG = {
    "docker_client_version": DEFAULT_DOCKER_API_VERSION,
    "docker_client_timeout": DEFAULT_DOCKER_CLIENT_TIMEOUT,
    "docker_registry": DEFAULT_DOCKER_REGISTRY_URL,
    "docker_hub": DEFAULT_DOCKER_HUB,
    "auth_server": DEFAULT_AUTH_SERVER_URL,
    "app_registry": DEFAULT_APP_REGISTRY_URL,
    "platform_url": DEFAULT_PLATFORM_URL,
    "log_level": DEFAULT_LOG_LEVEL
}


CGC_CONFIG = {
    "docker_client_version": DEFAULT_DOCKER_API_VERSION,
    "docker_client_timeout": DEFAULT_DOCKER_CLIENT_TIMEOUT,
    "docker_registry": CGC_DOCKER_REGISTRY_URL,
    "docker_hub": DEFAULT_DOCKER_HUB,
    "auth_server": CGC_AUTH_SERVER_URL,
    "gk_auth_server": CGC_GK_AUTH_SERVER_URL,
    "app_registry": CGC_APP_REGISTRY_URL,
    "platform_url": CGC_PLATFORM_URL,
    "log_level": DEFAULT_LOG_LEVEL
}


def read_config(path):
    cfg = {}
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                cfg = json.load(f)
        except Exception:
            print('Error loading config from %s.' % path)
    return cfg


def load_config(env):
    if env == 'SBG':
        cfg = DEFAULT_CONFIG
    elif env == 'CGC':
        cfg = CGC_CONFIG
    config_path = os.environ.get('SBG_CONFIG_FILE', None)
    if config_path:
        external_config = read_config(config_path)
    else:
        external_config = read_config(DEFAULT_CONFIG_PATH)
    cfg.update(external_config)
    log_level = cfg.get('log_level')
    logging.basicConfig(level=log_level)
    return Config(cfg)


CGC_TOKEN = ""


class Config(dict):

    def __getattr__(self, attr):
        return self.get(attr)

    __setattr__= dict.__setitem__

    __delattr__= dict.__delitem__
