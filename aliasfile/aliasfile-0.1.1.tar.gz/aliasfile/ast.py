"""Abstract Syntax Tree structures for parsing configuration file
"""


def _arg_dict(value):
    ret = {}
    if value is not None:
        ret.update(value)
    return ret


class Aliasfile:
    def __init__(self, commands=None, env=None):
        self.commands = _arg_dict(commands)
        self.env = _arg_dict(env)


class CommandSpec:
    def __init__(self, name, command=None, append_args=True,
                 env=None):

        self.name = name
        self.command = command or []
        self.append_args = append_args
        self.env = _arg_dict(env)
