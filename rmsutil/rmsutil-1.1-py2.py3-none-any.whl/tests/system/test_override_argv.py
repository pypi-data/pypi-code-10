import argparse
import sys

import pytest

import rmsutil.system


def test_override_argv():
    def assert_absent():
        assert '--cats' not in sys.argv
        assert '99' not in sys.argv

    assert_absent()

    process_name = sys.argv[0]

    # NOTE(kgriffs): argparse is OK with args of type unicode,
    #   so override_argv isn't strict about it either.
    with rmsutil.system.override_argv(
        u'--cats', 'yes',
        '--answer', u'42',
    ):
        assert sys.argv[0] == process_name
        assert '--cats' in sys.argv
        assert 'yes' in sys.argv

        parser = argparse.ArgumentParser()
        parser.add_argument('--cats')
        parser.add_argument('--answer', type=int)

        args = parser.parse_args()
        assert args.cats == 'yes'
        assert args.answer == 42

        with rmsutil.system.override_argv():
            # Only the process name should remain
            assert len(sys.argv) == 1
            assert sys.argv[0] == process_name

        with rmsutil.system.override_argv('-v'):
            assert len(sys.argv) == 2
            assert sys.argv[0] == process_name
            assert '-v' in sys.argv

    assert_absent()


def test_override_argv_raised():
    with pytest.raises(Exception):
        with rmsutil.system.override_argv('--cats'):
            assert '--cats' in sys.argv
            raise Exception()

    assert '--cats' not in sys.argv


def test_override_argv_requires_string_values():
    with pytest.raises(TypeError):
        with rmsutil.system.override_argv(1234):
            pass

    with pytest.raises(TypeError):
        with rmsutil.system.override_argv('-x', 1234):
            pass
