import os

import pytest

import rmsutil.system


def test_update_env():
    def assert_absent():
        assert 'OLIVAW_HOST' not in os.environ
        assert 'OLIVAW_USERNAME' not in os.environ
        assert 'OLIVAW_PASSWORD' not in os.environ

    assert_absent()

    with rmsutil.system.update_env(
        OLIVAW_HOST=u'127.0.0.1',  # os._Environ allows type unicode
        OLIVAW_USERNAME='user',
        OLIVAW_PASSWORD='pwd',
    ):
        assert os.environ['OLIVAW_HOST'] == '127.0.0.1'
        assert os.environ['OLIVAW_USERNAME'] == 'user'
        assert os.environ['OLIVAW_PASSWORD'] == 'pwd'

        with rmsutil.system.update_env(OLIVAW_PASSWORD='overridden'):
            assert os.environ['OLIVAW_PASSWORD'] == 'overridden'

        assert os.environ['OLIVAW_PASSWORD'] == 'pwd'

    assert_absent()


def test_no_side_effects():
    with rmsutil.system.update_env(OLIVAW_TEST_VALUE='abcd'):
        pass

    os.environ['OLIVAW_TEST_VALUE'] = '1234'
    assert os.getenv('OLIVAW_TEST_VALUE') == '1234'

    del os.environ['OLIVAW_TEST_VALUE']
    assert os.getenv('OLIVAW_TEST_VALUE') is None

    with pytest.raises(TypeError):
        os.environ['OLIVAW_TEST_VALUE'] = 1234


def test_update_env_raises():
    with pytest.raises(Exception):
        with rmsutil.system.update_env(
            OLIVAW_HOST='127.0.0.1',
        ):
            assert os.environ['OLIVAW_HOST'] == '127.0.0.1'
            raise Exception()

    assert 'OLIVAW_HOST' not in os.environ


def test_update_env_requires_string_values():
    with pytest.raises(TypeError):
        with rmsutil.system.update_env(NAME=1234):
            pass
