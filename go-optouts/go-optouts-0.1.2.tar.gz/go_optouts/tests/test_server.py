import yaml

from twisted.internet.defer import inlineCallbacks
from twisted.web.server import Site

from confmodel.errors import ConfigError

from vumi.tests.helpers import VumiTestCase, PersistenceHelper

from go_optouts.server import (
    HealthResource, read_yaml_config, ApiSiteConfig, ApiSite)
from go_optouts.auth import RequestHeaderAuth, BouncerAuth
from go_optouts.store.memory import MemoryOptOutBackend
from go_optouts.store.riak import RiakOptOutBackend
from go_optouts.tests.utils import SiteHelper


class TestHealthResource(VumiTestCase):

    @inlineCallbacks
    def setUp(self):
        self.site = Site(HealthResource())
        self.site_helper = yield self.add_helper(SiteHelper(self.site))

    @inlineCallbacks
    def test_health_resource(self):
        result = yield self.site_helper.get('/')
        self.assertEqual(result.code, 200)
        body = yield result.text()
        self.assertEqual(body, "OK")


class TestReadYamlConfig(VumiTestCase):

    def mk_config(self, data):
        path = self.mktemp()
        with open(path, "wb") as f:
            f.write(yaml.safe_dump(data))
        return path

    def test_read_config(self):
        path = self.mk_config({
            "foo": "bar",
        })
        data = read_yaml_config(path)
        self.assertEqual(data, {
            "foo": "bar",
        })

    def test_optional_config(self):
        data = read_yaml_config(None)
        self.assertEqual(data, {})


class TestApiSiteConfig(VumiTestCase):

    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    def test_backend_memory(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        self.assertEqual(cfg.backend, "memory")

    def test_backend_riak(self):
        cfg = ApiSiteConfig({"backend": "riak"})
        self.assertEqual(cfg.backend, "riak")

    def test_backend_required(self):
        err = self.assertRaises(ConfigError, ApiSiteConfig, {})
        self.assertEqual(str(err), "Missing required config field 'backend'")

    def test_unknown_backend(self):
        err = self.assertRaises(ConfigError, ApiSiteConfig, {"backend": "bad"})
        self.assertEqual(str(err), "Backend must be one of: riak, memory")

    def test_backend_config(self):
        cfg = ApiSiteConfig({"backend": "memory", "backend_config": {
            "camelot": "ham",
        }})
        self.assertEqual(cfg.backend_config, {"camelot": "ham"})

    def test_backend_config_optional(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        self.assertEqual(cfg.backend_config, {})

    def test_url_path_prefix(self):
        cfg = ApiSiteConfig({
            "backend": "memory", "url_path_prefix": "flashing/red/light"})
        self.assertEqual(cfg.url_path_prefix, "flashing/red/light")

    def test_url_path_prefix_optional(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        self.assertEqual(cfg.url_path_prefix, "optouts")

    def test_auth_bouncer_url(self):
        cfg = ApiSiteConfig({
            "backend": "memory", "auth_bouncer_url": "http://example.com/"})
        self.assertEqual(cfg.auth_bouncer_url, "http://example.com/")

    def test_auth_bouncer_url_optional(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        self.assertEqual(cfg.auth_bouncer_url, None)

    def test_create_backend_memory(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        backend = cfg.create_backend()
        self.assertTrue(isinstance(backend, MemoryOptOutBackend))

    def test_create_backend_riak(self):
        backend_config = self.persistence_helper.mk_config({})['riak_manager']
        cfg = ApiSiteConfig({
            "backend": "riak",
            "backend_config": backend_config,
        })
        backend = cfg.create_backend()
        self.assertTrue(isinstance(backend, RiakOptOutBackend))

    def test_create_auth_request_headers(self):
        cfg = ApiSiteConfig({"backend": "memory"})
        auth = cfg.create_auth()
        self.assertTrue(isinstance(auth, RequestHeaderAuth))

    def test_create_auth_bouncer(self):
        cfg = ApiSiteConfig({
            "backend": "memory", "auth_bouncer_url": "http://example.com/"})
        auth = cfg.create_auth()
        self.assertTrue(isinstance(auth, BouncerAuth))
        self.assertEqual(auth._auth_bouncer_url, "http://example.com")


class TestApiSite(VumiTestCase):

    def setUp(self):
        self.persistence_helper = self.add_helper(
            PersistenceHelper(use_riak=True, is_sync=False))

    def mk_config(self, data):
        path = self.mktemp()
        with open(path, "wb") as f:
            f.write(yaml.safe_dump(data))
        return path

    def mk_api_site(self, config=None):
        if config is None:
            config = {}
        if "backend" not in config:
            config["backend"] = "memory"
        return ApiSite(self.mk_config(config))

    def mk_server(self, config=None):
        api_site = self.mk_api_site(config)
        return self.add_helper(
            SiteHelper(api_site.site))

    @inlineCallbacks
    def test_health(self):
        site_helper = yield self.mk_server()
        result = yield site_helper.get('/health')
        self.assertEqual(result.code, 200)
        body = yield result.text()
        self.assertEqual(body, "OK")

    @inlineCallbacks
    def test_opt_out(self):
        site_helper = yield self.mk_server()
        result = yield site_helper.get('/optouts/count', headers={
            "X-Owner-ID": "owner-1",
        })
        self.assertEqual(result.code, 200)
        data = yield result.json()
        self.assertEqual(data, {
            'opt_out_count': 0,
            'status': {
                'code': 200,
                'reason': 'OK',
            },
        })

    @inlineCallbacks
    def test_url_path_prefix(self):
        site_helper = yield self.mk_server({
            "url_path_prefix": "wombats"
        })
        result = yield site_helper.get('/wombats/count', headers={
            "X-Owner-ID": "owner-1",
        })
        self.assertEqual(result.code, 200)
        data = yield result.json()
        self.assertEqual(data, {
            'opt_out_count': 0,
            'status': {
                'code': 200,
                'reason': 'OK',
            },
        })

    def test_memory_backend(self):
        api_site = self.mk_api_site({"backend": "memory"})
        backend = api_site.api._backend
        self.assertTrue(isinstance(backend, MemoryOptOutBackend))

    def test_riak_backend(self):
        config = self.persistence_helper.mk_config({})['riak_manager']
        api_site = self.mk_api_site({
            "backend": "riak",
            "backend_config": config,
        })
        backend = api_site.api._backend
        self.assertTrue(isinstance(backend, RiakOptOutBackend))
        self.assertEqual(
            backend.riak_manager.bucket_prefix, config["bucket_prefix"])

    def test_auth_request_headers(self):
        api_site = self.mk_api_site({"backend": "memory"})
        auth = api_site.api._auth
        self.assertTrue(isinstance(auth, RequestHeaderAuth))

    def test_auth_bouncer(self):
        api_site = self.mk_api_site({
            "backend": "memory",
            "auth_bouncer_url": "http://example.com/",
        })
        auth = api_site.api._auth
        self.assertTrue(isinstance(auth, BouncerAuth))
        self.assertEqual(auth._auth_bouncer_url, "http://example.com")
