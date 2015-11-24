import os
import os.path as osp
import shutil
import tempfile
import unittest

from six import StringIO

from quaycon.config import (
    DEFAULT_CONFIG_FILES,
    load_config,
    save_config,
)
from . utils import merge_dir


class TestConfig(unittest.TestCase):
    ALL_CONFIGS = DEFAULT_CONFIG_FILES

    @classmethod
    def setUpClass(cls):
        paths = list(filter(osp.isfile, cls.ALL_CONFIGS))
        if any(paths):
            cls.temp_dir = tempfile.mkdtemp()
            home = osp.expanduser("~")
            for path in paths:
                rel_path = path[len(home) + 1:]
                rel_dir = osp.join(cls.temp_dir, osp.dirname(rel_path))
                if not osp.isdir(rel_dir):
                    os.makedirs(rel_dir)
                shutil.move(path, osp.join(cls.temp_dir, rel_path))

    @classmethod
    def tearDownClass(cls):
        temp_dir = getattr(cls, 'temp_dir', None)
        if temp_dir is not None:
            merge_dir(temp_dir, osp.expanduser("~"), force=True)

    def setUp(self):
        for path in filter(osp.isfile, self.ALL_CONFIGS):
            os.remove(path)

    def test_load_empty_config(self):
        self.assertEqual(load_config(), {})

    def test_load_from_unknown_path(self):
        load_config('/path/to/unknown/file.yml')

    def test_load_from_default_path(self):
        with open(DEFAULT_CONFIG_FILES[0], 'w') as ostr:
            self._write_dumb_config(ostr)
        self._check_dumb_config()

    def test_load_from_file_like(self):
        file_like = StringIO()
        self._write_dumb_config(file_like)
        file_like.seek(0, 0)
        self._check_dumb_config(file_like)

    def test_write_to_unknown_path(self):
        with self.assertRaises(OSError) as exc:
            save_config(self._config_dict(), '/path/to/unknown/file.yml')
        self.assertEqual(exc.exception.errno, 13)

    def test_write_to_directory(self):
        with self.assertRaises(IOError) as exc:
            save_config(self._config_dict(), osp.expanduser("~"))
        self.assertEqual(exc.exception.errno, 21)

    def test_write_to_default_path(self):
        save_config(self._config_dict())
        self.assertTrue(osp.isfile(DEFAULT_CONFIG_FILES[-1]))

    def test_write_to_existing_path(self):
        prev_config = 'some-text-which is not a config'
        with open(DEFAULT_CONFIG_FILES[0], 'w') as ostr:
            ostr.write(prev_config)
        save_config(self._config_dict())
        with open(DEFAULT_CONFIG_FILES[0]) as istr:
            self.assertFalse(istr.read().startswith(prev_config))

    def test_write_to_file_like(self):
        file_like = StringIO()
        save_config(self._config_dict(), file_like)
        self.assertTrue(file_like.getvalue().startswith('organizations:'))

    def _check_dumb_config(self, *args, **kwargs):
        self.assertEqual(
            load_config(*args, **kwargs),
            self._config_dict(),
        )

    @classmethod
    def _config_dict(cls):
        return {
            'organizations': {
                'foo': {
                    'repositories': {
                        'my_repo': None,
                    },
                },
                'quay.io/foo': {
                    'token': 'a_token',
                    'repositories': {
                        'my_quay_io_repo': None,
                    },
                },
            },
        }

    @classmethod
    def _write_dumb_config(cls, ostr):
        ostr.write('organizations:\n')
        ostr.write('  foo:\n')
        ostr.write('    repositories:\n')
        ostr.write('      my_repo:\n')
        ostr.write('  quay.io/foo:\n')
        ostr.write('    token: a_token\n')
        ostr.write('    repositories:\n')
        ostr.write('      my_quay_io_repo:\n')
