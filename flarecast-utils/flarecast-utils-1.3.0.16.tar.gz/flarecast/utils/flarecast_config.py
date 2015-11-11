import json
from warnings import warn
import requests


class FlarecastConfig(object):
    __CONFIG_URL = 'https://dev.flarecast.eu/stash/projects/INFRA/repos/' \
                   'dev-infra/browse/global_config.json?&raw'

    def __init__(self, config_url=__CONFIG_URL):
        self.config_url = config_url
        self.config = {}

        requests.packages.urllib3.disable_warnings()

    def load(self):
        warn("Use 'load_from_url()' to load config file!", DeprecationWarning)
        self.load_from_url(self.config_url)

    def load_from_file(self, config_file):
        with open(config_file, "r") as cfg_file:
            data = cfg_file.readlines()
        self.config = json.loads(data)

    def load_from_url(self, config_url):
        config_resp = requests.get(config_url, verify=False)
        if config_resp.status_code != 200:
            print("Could not load global config file from %s" %
                  self.config_url)
            exit(1)
        self.config = config_resp.json()

    def __getattr__(self, name):
        return self.config.get(name, None)
