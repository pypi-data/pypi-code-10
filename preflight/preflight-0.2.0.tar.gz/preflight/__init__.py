from .config import read_config, run_test_suite
from .version import version as __version__


__all__ = ['__version__', 'run_from_file']


def run_from_file(file_name):
    test_suite = read_config(file_name)
    run_test_suite(test_suite)
