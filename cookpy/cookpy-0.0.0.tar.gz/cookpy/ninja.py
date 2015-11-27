# -*- coding: utf-8 -*-

io = None


def _line(text='', indent=0):
    io.write('{}{}\n'.format('  ' * indent, text))


def build(inputs, description, command, outputs, after=None, depfile=None,
          deps=None, msvc_deps_prefix=None, generator=False, restat=False,
          rspfile=None, rspfile_content=None):
    """ Build...

    @type inputs: list[str]
    @type description: str
    @type command: str
    @type outputs: list[str]
    @type after: list[str]
    @type depfile: str
    @type deps: str
    @type msvc_deps_prefix: str
    @type generator: bool
    @type restat: bool
    @type rspfile: str
    @type rspfile_content: str
    """
    if isinstance(outputs, str):
        raise TypeError('outputs must be a list, not string')
    if isinstance(inputs, str):
        raise TypeError('inputs must be a list, not string')
    if isinstance(after, str):
        raise TypeError('after must be a list, not string')

    inputs = ' '.join(map(_escape_path, inputs))
    outputs = ' '.join(map(_escape_path, outputs))
    if not after:
        after = ''
    else:
        after = ' || {}'.format(' '.join(map(_escape_path, after)))

    variables = {'with': command, 'as': description}
    if depfile is not None:
        variables['depfile'] = depfile
    if deps is not None:
        variables['deps'] = deps
    if msvc_deps_prefix is not None:
        variables['msvc_deps_prefix'] = msvc_deps_prefix
    if generator:
        variables['generator'] = 'True'
    if restat:
        variables['restat'] = 'True'
    if rspfile is not None:
        variables['rspfile'] = rspfile
    if rspfile_content is not None:
        variables[rspfile_content] = rspfile_content

    _line()
    _line('build {}: from {}{}'.format(outputs, inputs, after))
    for key, value in variables.items():
        _line('{} = {}'.format(key, value), indent=1)


def _escape_path(path):
    return path.replace('$ ', '$$ ').replace(' ', '$ ').replace(':', '$:')
