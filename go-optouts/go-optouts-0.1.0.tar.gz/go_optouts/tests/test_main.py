from vumi.tests.helpers import VumiTestCase

from click.testing import CliRunner

from go_optouts.server import ApiSite
from go_optouts.store.memory import MemoryOptOutBackend
from go_optouts.main import run


class TestCli(VumiTestCase):
    def setUp(self):
        self.run_calls = []

        def record_site_run(*args):
            self.run_calls.append(args)

        self.patch(ApiSite, 'run', record_site_run)

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(run, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("Vumi Go Opt Out API." in result.output)
        self.assertTrue(
            "-c, --config TEXT   YAML config file" in result.output)
        self.assertTrue(
            "-h, --host TEXT     Host to listen on" in result.output)
        self.assertTrue(
            "-p, --port INTEGER  Port to listen on" in result.output)

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(run, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("go-optouts, version " in result.output)

    def test_config_required(self):
        runner = CliRunner()
        result = runner.invoke(run, [])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue('Missing option "--config" / "-c".' in result.output)

    def test_run(self):
        cfg_file = self.mktemp()
        with open(cfg_file, "wb") as f:
            f.write("backend: memory")
        runner = CliRunner()
        result = runner.invoke(run, [
            '--config', cfg_file,
            '--host', '127.0.0.1',
            '--port', '8000',
        ])
        self.assertEqual(result.exit_code, 0)
        [run_call] = self.run_calls
        [site, host, port] = run_call
        self.assertTrue(isinstance(site.api._backend, MemoryOptOutBackend))
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 8000)

    def test_run_default_parameters(self):
        cfg_file = self.mktemp()
        with open(cfg_file, "wb") as f:
            f.write("backend: memory")
        runner = CliRunner()
        result = runner.invoke(run, [
            '--config', cfg_file,
        ])
        self.assertEqual(result.exit_code, 0)
        [run_call] = self.run_calls
        [site, host, port] = run_call
        self.assertTrue(isinstance(site.api._backend, MemoryOptOutBackend))
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 8080)
