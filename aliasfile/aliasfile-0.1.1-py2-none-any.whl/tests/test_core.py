# import pytest
# from unittest import mock

# from aliasfile.core import Command, Configuration, _TrackGetitem


# class TestConfiguration:

#     @pytest.yield_fixture
#     def mock_env(self):
#         with mock.patch('os.environ', new={'USER': 'base_user'}):
#             yield

#     def test_environment_is_updated_correctly(self):
#         config = Configuration(
#             env={'OVERRIDE': 'new', 'EXTRA': 'extra'},
#             base_env={'OVERRIDE': 'old', 'BLAH': 'spam!'})

#         assert config.get_env() == {
#             'OVERRIDE': 'new', 'EXTRA': 'extra', 'BLAH': 'spam!'}

#     def test_env_is_copied(self):
#         env = {'foo': 'bar'}
#         config = Configuration(env=env, base_env={})
#         assert config.get_env() == {'foo': 'bar'}
#         env['BAR'] = 'BAZ'
#         assert config.get_env() == {'foo': 'bar'}

#     def test_vars_are_copied(self):
#         vars = {'foo': 'bar'}
#         config = Configuration(vars=vars)
#         assert config.get_vars() == {'foo': 'bar'}
#         vars['BAR'] = 'BAZ'
#         assert config.get_vars() == {'foo': 'bar'}

#     def test_base_env_is_loaded_from_os_environ(self, mock_env):
#         config = Configuration()
#         assert config.get_env() == {'USER': 'base_user'}

#     def test_base_env_is_loaded_from_os_environ_and_merged(self, mock_env):
#         config = Configuration(env={'USER': 'somebody'})
#         assert config.get_env() == {'USER': 'somebody'}

#     def test_get_env_inheritance_works(self):
#         config = Configuration(base_env={'A': 'a1', 'B': 'b1'},
#                                env={'B': 'b2', 'C': 'c2'})
#         assert config.get_env() == {'A': 'a1', 'B': 'b2', 'C': 'c2'}

#     class Test_from_config:

#         def test_with_empty_config(self, mock_env):
#             config = Configuration.from_config({})
#             assert config.commands == {}
#             assert config.get_env() == {'USER': 'base_user'}
#             assert config.get_vars() == {}

#         def test_commands_are_loaded(self):
#             config = Configuration.from_config(
#                 {'commands': {'cmd1': 'rm -rf /'}})
#             assert config.commands == {
#                 'cmd1': Command.from_config(config, 'cmd1', 'rm -rf /')}

#         def test_env_is_loaded(self, mock_env):
#             config = Configuration.from_config({'env': {'EXTRA': 'hello'}})
#             assert config.raw_env == {'EXTRA': 'hello'}
#             assert config.get_env() == {'USER': 'base_user', 'EXTRA': 'hello'}

#         def test_vars_are_loaded(self):
#             config = Configuration.from_config({'vars': {'FOO': 'bar'}})
#             assert config.raw_vars == {'FOO': 'bar'}
#             assert config.get_vars() == {'FOO': 'bar'}


# class TestCommand:

#     @pytest.fixture
#     def config(self):
#         return Configuration()

#     class Test_from_config:

#         def test_initialize_from_string(self, config):
#             cmd = Command.from_config(config, 'mycommand', 'foo "bar baz"')
#             assert cmd.config is config
#             assert cmd.name == 'mycommand'
#             assert cmd.raw_command == ['foo', 'bar baz']

#         def test_initialize_from_bytes(self, config):
#             cmd = Command.from_config(config, 'mycommand', b'foo "bar baz"')
#             assert cmd.config is config
#             assert cmd.name == 'mycommand'
#             assert cmd.raw_command == ['foo', 'bar baz']

#         @pytest.mark.parametrize('value', [123, True, ['foo'], None],
#                                  ids=lambda x: repr(x))
#         def test_from_config_invalid_raises_typeerror(self, config, value):
#             with pytest.raises(TypeError):
#                 Command.from_config(config, 'mycommand', value)

#         def test_from_config_dict(self, config):
#             cmd = Command.from_config(config, 'mycommand', {
#                 'command': 'foo "bar baz"',
#                 'env': {'ENV1': 'env1'},
#                 'vars': {'VAR1': 'var1'},
#             })
#             assert cmd.config is config
#             assert cmd.name == 'mycommand'
#             assert cmd.raw_command == ['foo', 'bar baz']
#             assert cmd.raw_env == {'ENV1': 'env1'}
#             assert cmd.raw_vars == {'VAR1': 'var1'}

#     class Test_replacement_in_command:

#         def test_args_are_replaced(self, config):
#             cmd = Command(config, 'mycommand', ['foo', '{args[0]}'])
#             assert cmd.get_command(['BAR']) == ['foo', 'BAR']

#         def test_args_are_replaced_partial(self, config):
#             cmd = Command(config, 'mycommand', ['foo', '--file={args[0]}'])
#             assert cmd.get_command(['BAR']) == ['foo', '--file=BAR']

#         def test_positional_args_are_replaced(self, config):
#             cmd = Command(config, 'mycommand', ['foo', '{}'])
#             assert cmd.get_command(['BAR']) == ['foo', 'BAR']

#             cmd = Command(config, 'mycommand', ['foo', '{0}'])
#             assert cmd.get_command(['BAR']) == ['foo', 'BAR']

#     def test_environment_from_os_environ_is_replaced(self, config):
#         config = Configuration(base_env={'USER': 'base_user'})
#         cmd = Command(config, 'mycommand', ['foo', '{env[USER]}'])
#         assert cmd.get_command([]) == ['foo', 'base_user']


# class TestTrackGetitem:

#     def test_getitems_are_recorded_correctly(self):
#         trk = _TrackGetitem(['foo', 'bar', 'baz'])
#         assert trk.history == []
#         trk[0]
#         trk[1]
#         assert trk.history == [0, 1]
