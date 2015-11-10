import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web import http
from twisted.web.resource import Resource

from confmodel import Config
from confmodel.fields import ConfigText, ConfigDict

from vumi.utils import build_web_site

import yaml

from .api import API
from .auth import RequestHeaderAuth, BouncerAuth
from .store.memory import MemoryOptOutBackend
from .store.riak import RiakOptOutBackend


class HealthResource(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setResponseCode(http.OK)
        request.do_not_log = True
        return 'OK'


def read_yaml_config(config_file):
    """Parse a YAML config file."""
    if config_file is None:
        return {}
    with file(config_file, 'r') as stream:
        # Assume we get a dict out of this.
        return yaml.safe_load(stream)


class ApiSiteConfig(Config):

    BACKENDS = {
        "memory": MemoryOptOutBackend,
        "riak": RiakOptOutBackend,
    }

    backend = ConfigText(
        "Optout backend to use. One of 'memory' or 'riak'",
        required=True)

    backend_config = ConfigDict(
        "Configuration for backend.",
        default={})

    auth_bouncer_url = ConfigText(
        "URL to bounce requests to for authentication",
        default=None)

    url_path_prefix = ConfigText(
        "URL path prefix for the optout API.",
        default="optouts")

    def post_validate(self):
        if self.backend not in self.BACKENDS:
            self.raise_config_error(
                "Backend must be one of: %s" % ", ".join(self.BACKENDS.keys()))

    def create_backend(self):
        return self.BACKENDS[self.backend].from_config(self.backend_config)

    def create_auth(self):
        if self.auth_bouncer_url:
            return BouncerAuth(self.auth_bouncer_url)
        return RequestHeaderAuth()


class ApiSite(object):
    """ Site for serving the opt out API. """

    def __init__(self, config_file=None):
        self.config = ApiSiteConfig(read_yaml_config(config_file))
        self.api = API(
            self.config.create_backend(),
            self.config.create_auth())
        self.site = build_web_site({
            'health': HealthResource(),
            self.config.url_path_prefix: self.api.app.resource(),
        })

    def run(self, host, port):
        log.startLogging(sys.stdout)
        reactor.listenTCP(port, self.site, interface=host)
        reactor.run()
