import os
import shlex

from .utils import _print_command


class _Auto:
    def __repr__(self):
        return 'AUTO'

AUTO = _Auto()


class Configuration:
    def __init__(self, commands=None, env=None, vars=None,
                 base_env=None):

        self.commands = {}
        if commands is not None:
            self.commands.update(commands)

        self.base_env = {}
        if base_env is not None:
            self.base_env.update(base_env)

        self.raw_env = {}
        if env is not None:
            self.raw_env.update(env)

        self.raw_vars = {}
        if vars is not None:
            self.raw_vars.update(vars)

    @classmethod
    def from_config(cls, config):
        obj = cls(
            commands={},
            env=config.get('env', {}),
            vars=config.get('vars', {}))

        obj.commands.update({
            key: Command.from_config(obj, name=key, spec=cfg)
            for key, cfg in config.get('commands', {}).items()})

        return obj

    @property
    def env(self):
        env = self.base_env.copy()
        env.update(self.raw_env)
        return env

    @property
    def vars(self):
        return self.raw_vars.copy()

    # def run(self, args):
    #     cmd, *args = args
    #     self.commands[cmd].run(args)

    # def get_env(self):
    #     env = self.base_env.copy()
    #     env.update(self.raw_env)
    #     return env

    # def get_vars(self):
    #     return self.raw_vars.copy()

    def __repr__(self):
        return ('Config(commands={0.commands!r}, env={0.env!r}, '
                'vars={0.vars!r}, base_env={0.base_env!r})'
                .format(self))


class Command:
    def __init__(self, config, name, command, env=None, vars=None,
                 append_extra_args=AUTO):

        self.config = config
        self.name = name

        self.raw_command = command
        self.raw_env = env if env is not None else {}
        self.raw_vars = vars if vars is not None else {}
        self.append_extra_args = append_extra_args

    def __repr__(self):
        return ('Command(name={0.name!r}, command={0.raw_command!r}, '
                'env={0.raw_env!r}, vars={0.raw_vars!r}, '
                'append_extra_args={0.append_extra_args!r})'
                .format(self))

    @classmethod
    def from_config(cls, config, name, spec):

        if isinstance(spec, (str, bytes)):
            return cls.from_config(config, name, {'command': spec})

        if not isinstance(spec, dict):
            raise TypeError('Unsupported command spec type')

        command = spec['command']
        if isinstance(command, bytes):
            command = command.decode()

        if isinstance(command, str):
            command = shlex.split(command)

        command = list(command)

        return cls(
            config, name, command=command,
            env=spec.get('env') or {},
            vars=spec.get('vars') or {},
            append_extra_args=spec.get('append_extra_args', AUTO))

    def get_command(self, args):
        _args = _TrackGetitem(args)
        context = {
            'args': _args,
            'env': self.get_env(args),
            'vars': self.get_vars(args),
        }
        command = self._substitute_list(self.raw_command, context)

        if self.append_extra_args is AUTO:
            append_extra_args = (len(_args.history) == 0)
        else:
            append_extra_args = self.append_extra_args

        if append_extra_args:
            command.extend(args)

        return command

    def get_env(self, args):
        context = {
            'args': args,
            'env': self.config.get_env(),
            'vars': self.get_vars(args),
        }
        return self._substitute_dict(self.raw_env, context)

    def get_vars(self, args):
        context = {
            'args': args,
            'env': self.config.get_env(),
            'vars': self.config.get_vars(),
        }
        return self._substitute_dict(self.raw_vars, context)

    def run(self, args):
        cmd = self.get_command(args)
        env = os.environ.copy()
        env.update(self.get_env(args))
        _print_command(cmd)

        os.execvpe(cmd[0], cmd, env)

    def _substitute2(self, text, context):
        args = context.get('args') or ()
        return text.format(*args, **context)

    def _substitute_dict(self, data, context):
        return {key: self._substitute2(val, context)
                for key, val in data.items()}

    def _substitute_list(self, data, context):
        return [self._substitute2(val, context) for val in data]

    def __eq__(self, other):
        return ((type(self) == type(other)) and
                (other.__dict__ == self.__dict__))


class _TrackGetitem(list):
    def __init__(self, obj):
        super().__init__(obj)
        self.history = []

    def __getitem__(self, key):
        self.history.append(key)
        return super().__getitem__(key)
