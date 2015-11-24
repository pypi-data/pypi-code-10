import os.path as osp
import unittest

from six import StringIO

from quaycon.cli import touch_command, discover_command
from quaycon.config import load_config, save_config
from . utils import vcr


class TestTouch(unittest.TestCase):
    CONFIG_FILE = osp.splitext(__file__)[0] + '.yaml'

    @vcr.use_cassette
    def test_touch(self):
        repo = 'quay.io/cogniteev/docido-contrib-crawlers:latest'
        builds = list(touch_command(repo, self.CONFIG_FILE))
        self.assertEqual(len(builds), 1)
        self.assertEqual(
            builds[0].get('repository'),
            {
                'namespace': 'cogniteev',
                'name': 'docido-pull-crawler-github',
            }
        )
        self.assertEqual(builds[0].get('tags'), ['develop', 'latest'])

    @vcr.use_cassette
    def test_wait_touch(self):
        repo = 'quay.io/cogniteev/docido-contrib-crawlers:latest'
        builds = list(touch_command(repo, self.CONFIG_FILE, wait=1))
        self.assertTrue(len(builds), 1)
        self.assertEqual(builds[0].get('phase'), 'complete')

    @vcr.use_cassette
    def test_recursive_wait(self):
        builds = list(touch_command('python:2.7', self.CONFIG_FILE,
                                    wait=1, recursive=True))
        self.assertEqual(len(builds), 2)

    @vcr.use_cassette
    def test_discover(self):
        org = 'quay.io/cogniteev'
        truncated_config = StringIO()
        config = load_config(self.CONFIG_FILE)
        config['organizations'][org]['repositories'] = None
        save_config(config, truncated_config)
        truncated_config.seek(0, 0)
        discover_command(['cogniteev'], truncated_config, interactive=False)
        config = load_config(self.CONFIG_FILE)
        tags = config.get('organizations', {})\
            .get('quay.io/cogniteev', {})\
            .get('repositories', {})\
            .get('docido-contrib-crawlers', {})\
            .get('on_build', {})\
            .get('tags', {})
        self.assertEqual(len(tags), 1)
        latest_trigger = tags.get('latest')
        self.assertEqual(len(latest_trigger), 1)
        github_repo = 'quay.io/cogniteev/docido-pull-crawler-github'
        self.assertEqual(
            latest_trigger.get(github_repo),
            [
                dict(trigger_uuid="dcb1e958-9fdb-4e9b-9856-4d52771b3df9",
                     ref="refs/heads/develop")
            ]
        )


if __name__ == '__main__':
    unittest.main()
