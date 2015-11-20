# coding=utf8

import os
import json
import yaml
from imp import load_module


class ConfigParsedError(Exception):
    """
    The runtime-exception for config parser.
    """
    pass


def parse(stream=None, parser=None, **kwargs):
    """
    Parse config from stream of config file.

    :param stream: input stream object
    :param parser: parser class with load method

    **Parser Example**

    .. code-block:: python

        from toolkit.config import Parser

        class JsonParser(Parser):
            def __init__(self, to_object=False, *args, **kwargs):
                super(JsonParser, self).__init__(to_object=to_object, *args, **kwargs)

            def load(self, stream, *args, **kwargs):
                return self.make_result(json.load(stream, *args, **kwargs))
    """
    if not stream:
        raise ConfigParsedError('Stream Error.')
    if parser:
        return parser(**kwargs).load(stream)

    sname = getattr(stream, 'name', None)
    if not any([sname, parser]):
        sname = '.json'
    if '.' not in stream.name:
        raise ConfigParsedError('Unknown type of config file.')

    name, suffix = sname.rsplit('.', 1)
    if suffix == 'py':
        return imp.load_module(name, stream.name)
    elif suffix == 'json':
        return JsonParser(**kwargs).load(stream)
    elif suffix in ('yaml', 'yml'):
        return YamlParser(**kwargs).load(stream)
    else:
        return {}


def parse_file(path, **kwargs):
    """
    Parse config from path of config file.

    :param path: path of input file.
    :param kwargs: keyword argument for :func:`parse` function.
    """
    with open(path) as f:
        return parse(f, **kwargs)


class Parser(object):
    def __init__(self, to_object=False, *args, **kwargs):
        self._obj = to_object

    def make_result(self, config):
        if self._obj:
            Config = type('Config', (dict,), config)
            obj = Config()
            obj.update(config)
            return obj
        return config


class YamlParser(Parser):
    def load(self, stream):
        return self.make_result(yaml.load(stream) or {})


class JsonParser(Parser):
    def load(self, stream, *args, **kwargs):
        return self.make_result(json.load(stream, *args, **kwargs))

    def loads(self, string, *args, **kwargs):
        return self.make_result(json.loads(string, *args, **kwargs))

    def __str__(self):
        return json.dumps(self)
