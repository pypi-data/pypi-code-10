import os
from unittest import mock

import pytest

from aliasfile.parse import parse_configuration
from aliasfile.runner import run_command


class Test_run_command:

    @pytest.yield_fixture(autouse=True)
    def mock_execvpe(self):
        with mock.patch('os.execvpe') as mocked:
            yield mocked

    def test_simple_command_would_be_run(self, mock_execvpe):
        config = parse_configuration({
            'commands': {
                'foo': {
                    'command': 'echo "foo bar"',
                    'env': {'ONE': '1'},
                }
            }
        })

        run_command(config, 'foo', [], env={'USER': 'foo'})

        assert mock_execvpe.call_args_list == [
            mock.call('echo', ['echo', 'foo bar'],
                      {'USER': 'foo', 'ONE': '1'})]

    def test_extra_args_are_appended_by_default(self, mock_execvpe):
        config = parse_configuration({
            'commands': {
                'foo': {
                    'command': 'echo "foo bar"',
                }
            }
        })

        run_command(config, 'foo', ['extra', 'args'], env={})

        assert mock_execvpe.call_args_list == [
            mock.call('echo', ['echo', 'foo bar', 'extra', 'args'], {})]

    def test_extra_args_are_not_appended_if_disabled(self, mock_execvpe):
        config = parse_configuration({
            'commands': {
                'foo': {
                    'command': 'echo "foo bar"',
                    'append_args': False,
                }
            }
        })

        run_command(config, 'foo', ['extra', 'args'], env={})

        assert mock_execvpe.call_args_list == [
            mock.call('echo', ['echo', 'foo bar'], {})]

    def test_args_and_env_can_be_omitted(self, mock_execvpe):
        config = parse_configuration({
            'commands': {
                'foo': {
                    'command': 'echo "foo bar"',
                }
            }
        })

        run_command(config, 'foo')

        assert mock_execvpe.call_args_list == [
            mock.call('echo', ['echo', 'foo bar'], os.environ)]

    def test_command_can_be_empty(self, mock_execvpe):
        config = parse_configuration({'commands': {'foo': None}})

        run_command(config, 'foo', ['echo', 'foo bar'], {})

        assert mock_execvpe.call_args_list == [
            mock.call('echo', ['echo', 'foo bar'], {})]

    class Test_replacements_in_command:

        def test_replacements_are_applied_to_command(self, mock_execvpe):
            config = parse_configuration({
                'commands': {
                    'foo': {'command': 'echo "foo {0}"',
                            'append_args': False}
                }
            })

            run_command(config, 'foo', ['ARG'], {})

            assert mock_execvpe.call_args_list == [
                mock.call('echo', ['echo', 'foo ARG'], {})]

        def test_replacements_are_not_applied_to_args(self, mock_execvpe):
            config = parse_configuration({
                'commands': {
                    'foo': {'command': 'echo',
                            'append_args': True}
                }
            })

            run_command(config, 'foo', ['ARG {0}'], {})

            assert mock_execvpe.call_args_list == [
                mock.call('echo', ['echo', 'ARG {0}'], {})]
