from aliasfile.parse import parse_configuration
from aliasfile.ast import Aliasfile, CommandSpec


class Test_parse_configuration:

    def test_empty_configuration(self):
        cfg = parse_configuration({})
        assert isinstance(cfg, Aliasfile)
        assert cfg.commands == {}
        assert cfg.env == {}

    class Test_parse_command_spec:

        def test_command_as_string(self):
            cfg = parse_configuration({
                'commands': {'foo': 'some foo command'}})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == ['some', 'foo', 'command']

        def test_command_as_bytes(self):
            cfg = parse_configuration({
                'commands': {'foo': b'some foo command'}})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == ['some', 'foo', 'command']

        def test_command_as_list(self):
            cfg = parse_configuration({
                'commands': {'foo': ['some', 'foo', 'command']}})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == ['some', 'foo', 'command']

        def test_command_as_tuple(self):
            cfg = parse_configuration({
                'commands': {'foo': ('some', 'foo', 'command')}})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == ['some', 'foo', 'command']

        def test_command_can_be_none(self):
            cfg = parse_configuration({'commands': {'foo': None}})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == []

        def test_command_as_dict(self):
            cfg = parse_configuration({
                'commands': {
                    'foo': {
                        'command': 'echo "foo bar"',
                        'env': {'ENV1': 'val1'},
                    },
                }})

            assert isinstance(cfg, Aliasfile)
            assert isinstance(cfg.commands['foo'], CommandSpec)
            assert cfg.commands['foo'].command == ['echo', 'foo bar']
            assert cfg.commands['foo'].env == {'ENV1': 'val1'}
