# Released under GPL3 terms (see LICENSE)

"""Create templates from strings"""

from . import io
from i3barfodder.validation import str2num
import re
import operator
from collections import abc

# TODO: Many popular status bar screenshots have labels in front of CPU,
# network, etc displays. Maybe Template should have a 'label' argument?

# TODO: Maybe there is potential for better optimization: Instead of keeping
# separate templates for initialization and updates, keep track of which
# key=value pairs have already been sent and don't send them again in the next
# run unless they've changed.  Only 'name' and 'instance' are obligatory.


class Template():
    _SPLITBLOCKS_REGEX = re.compile(r'('
                                    r'(?<!\\)\[.*?(?<!\\)\]'  # [...] if brackets are not escaped
                                    r'\d*\|?'                 # Optional separator defintion
                                    r')')

    def __init__(self, name, tmpltstr, min={}, max={}, softmin={}, softmax={}):
        self._blocks = []
        index = 0
        for blockstr in self._SPLITBLOCKS_REGEX.split(tmpltstr):
            if blockstr == '':
                continue
            index += 1
            blockid = str(name)+'_#'+str(index)

            # Enclose normal text with brackets to make it a valid block string
            if blockstr[0] != '[':
                blockstr = '[' + blockstr + ']'
            self._blocks.append(BlockTemplate(blockid, blockstr,
                                              min, max, softmin, softmax))

    def make_blocks(self, something, init=False):
        """
        Apply `something` to this template

        `something` can be:

          - a dictionary, which is passed to the `format` method of each
            string value of each block in this template. This creates a new
            list of blocks, which is returned.

          - a callable object, which is called with each string value of each
            block in this template to create a new list of blocks, which is
            returned.

          - a list/tuple/set of dictionaries/callables. In this case, each
            item is passed to this method recursively as described above. The
            resulting lists of blocks are concatenated (with `list.extend`)
            into a flat list and returned.

        If `init` is True, the returned blocks initialize things like dynamic
        colors and inline function calls (e.g. vbar()). If `init` is False,
        the returned blocks only update them with new values.
        """

        if isinstance(something, (list, tuple, set)):
            result = []
            for s in something:
                result.extend(self.make_blocks(s, init))
            return result

        else:
            if callable(something):
                fillin = something
            else:
                something = dict(something)
                def fillin(tmplt_text):
                    try:
                        return tmplt_text.format(**something)
                    except KeyError as e:
                        io.croak('Unknown field: {}\nKnown fields are: {}'
                                 .format(e, ', '.join(something.keys())))

            return [block.apply(fillin, init=init)
                    for block in self._blocks]


class BlockTemplate():
    _BLOCK_REGEX = re.compile(r'^\['                       # Start of block
                              r'(?P<text>.*?)'             # This becomes 'full_text'
                              r'(?:(?<!\\)\|'              # After unescaped '|' ...
                              r'(?P<colorspec>[^\]]+?)'    # ... optional dynamic color
                              r')?'                        # End of dynamic color
                              r'\]'                        # End of block
                              r'(?P<separator>\d*\|?)'     # Optional separator definition
                              r'$')

    def __init__(self, blockid, blockstr, min={}, max={}, softmin={}, softmax={}):
        self._update_template = dict(name=blockid)
        self._init_template = dict(name=blockid, separator=False,
                                   separator_block_width=0)

        blockmatch = self._BLOCK_REGEX.match(blockstr)
        if blockmatch is None:
            raise ValueError('Invalid block template string: {!r}'.format(blockstr))

        full_text = unescape(blockmatch.group('text'), chars='[]|')
        full_text_init, full_text_update = _parse_vbars(blockid, full_text,
                                                        min, max, softmin, softmax)
        self._init_template['full_text'] = full_text_init
        self._update_template['full_text'] = full_text_update

        # Optional dynamic color specification
        colorspec = blockmatch.group('colorspec')
        if colorspec is not None:
            dyncolor, dyncolor_value = \
                _parse_dyncolor(blockid, colorspec, min, max, softmin, softmax)
            self._init_template['color'] = dyncolor
            if dyncolor_value is not None:
                self._update_template['dyncolor_value'] = dyncolor_value

        # 'separator' and 'separator_block_width'
        sep = blockmatch.group('separator')
        self._init_template['separator'] = bool(sep and (sep[0] == '|' or sep[-1] == '|'))
        sep = sep.strip('|')
        if sep:
            try:
                self._init_template['separator_block_width'] = int(sep)
            except ValueError:
                raise ValueError('Invalid separator: {!r}'.format(sep))

        # io.debug('INIT: {}'.format(self._init_template))
        # io.debug('UPDATE: {}'.format(self._update_template))

    def apply(self, callback, init):
        """
        Use `callback` to create a new block

        Pass each string value in the template to `callback` and use its
        return value to replace the string.  This creates a new block that is
        finally returned.  Non-string values are copied shallowly.

        If `init` is True, initialize dynamic colors, vbars, etc. Otherwise
        just update them.
        """
        if init:
            block = self._init_template.copy()
        else:
            block = self._update_template.copy()

        for key,val in block.items():
            if type(val) is str:
                try:
                    block[key] = ConditionalString(callback(val))
                except ConditionError as e:
                    io.croak(e)
                except Exception as e:
                    import traceback
                    import pprint
                    io.debug(traceback.format_exc())
                    io.croak('Unknown fatal error while working on template:\n{}'
                             .format(pprint.pformat(tmplt)))

        # io.debug('Made a new block: {}\n'.format(block))
        return block


_FUNC_CALL_REGEX = re.compile(r'([vh]bar\([^\)]*?\))')
_FUNC_ARGS_REGEX = re.compile(r'\(([^\)]*?)\)')

def _parse_vbars(name, text, min={}, max={}, softmin={}, softmax={}):
    """
    Find vbar function calls in `text`, give them unique names, apply default
    limits to it and return `text` twice: once for initializing each bar and
    once for updating them.
    """
    limits = dict(min=min, max=max, softmin=softmin, softmax=softmax)

    def parse_arguments(string):
        args = [arg.strip() for arg in string.split(',') if arg]
        if len(args) < 1:
            io.croak('Missing field name in vbar call: {!r}'.format(text))

        field = args.pop(0)  # First argument is the field
        kwargs = dict(arg.split('=') for arg in args)  # The rest are keyword arguments
        return (field, kwargs)

    def make_init_call(bar_id, field, kwargs):
        init_args = field

        # Defaults
        for key in ('min', 'max', 'softmin', 'softmax'):
            if key in limits and field in limits[key]:
                init_args += ', {}={}'.format(key, limits[key][field])

        # User arguments
        for key,value in kwargs.items():
            init_args += ', {}={}'.format(key, value)

        callstr = 'vbar_{}:{}({})'.format(name, bar_id, init_args)
        # io.debug('Made new vbar init call: {}'.format(callstr))
        return callstr

    def make_update_call(bar_id, field, kwargs):
        callstr = 'vbar_{}:{}({})'.format(name, bar_id, field)
        # io.debug('Made new vbar update call: {}'.format(callstr))
        return callstr

    def make_calls(text):
        new_texts = []
        for make_call in (make_init_call, make_update_call):
            new_texts.append('')
            bar_counter = 0
            for part in _FUNC_CALL_REGEX.split(text):
                match = _FUNC_CALL_REGEX.match(part)
                if match is not None:
                    func_call = match.group(0)
                    bar_counter += 1
                    args = _FUNC_ARGS_REGEX.search(func_call).group(1)
                    args = parse_arguments(args)
                    new_texts[-1] += make_call(bar_counter, *args)
                elif part != '':
                    new_texts[-1] += part
        return tuple(new_texts)

    init_calls, update_calls = make_calls(text)
    return init_calls, update_calls


_COLORSPEC_REGEX = re.compile(r'^(?:(\S+?):)?(.*)$')

def _parse_dyncolor(name, dyncolorstr, min={}, max={}, softmin={}, softmax={}):
    """
    Apply default limits to dynamic color specification `dyncolorstr`

    Return the resulting full dynamic color specification and the field name
    to update it, if specified.
    """
    colormatch = _COLORSPEC_REGEX.match(dyncolorstr)
    if colormatch is None:
        io.croak('Invalid dynamic color spec: {}'.format(dyncolorstr))
    else:
        field = colormatch.group(1)
        color = colormatch.group(2)
        value = None
        if field is not None:
            if field in min:
                color = 'min=' + str(min[field]) + ':' + color
            if field in max:
                color = 'max=' + str(max[field]) + ':' + color
            if field in softmin:
                color = 'softmin=' + str(softmin[field]) + ':' + color
            if field in softmax:
                color = 'softmax=' + str(softmax[field]) + ':' + color
            color +=  ':value='+field
            value = field
        return color, value


class ConditionError(Exception):
    pass

class ConditionalString(str):
    """
    Normal string that resolves and replaces conditions

    A condition may appear anywhere in the string and looks like this:

        (SOMETHING?[=]CONDITION)

    The conditional is replaced with SOMETHING if CONDITION is true.  If the
    "?" is followed by a "=", the conditional is replaced with
    len(SOMETHING)*' '.

    CONDITION compares two numbers and uses `i3barfodder.str2num` to parse
    them. Comparison operators are: "<", ">", "<=", ">=", "=", "!="

    Escaping "(" or ")" prevents the conditional from being parsed.
    """
    def __new__(cls, string):
        # io.debug('Parsing conditions in: {!r}'.format(string))
        if '(' not in string:
            return string
        while True:
            start, end = cls._find_next_condition(string)
            if start is not None:
                # io.debug('Found conditional at {}:{}: {}'.format(start, end, string[start:end]))
                replacement = cls._apply_condition(string[start:end])
                string = ''.join((string[:start], replacement, string[end:]))
            else:
                return unescape(string, chars='()?')

    @staticmethod
    def _find_next_condition(string):
        start = -1
        for i,c in enumerate(string):
            if c == '(' and (i == 0 or string[i-1] != '\\'):
                start = i
            elif c == ')' and start >= 0 and string[i-1] != '\\':
                end = i+1
                if '?' in string[start:end]:
                    return (start, end)
        return (None, None)

    _CONDITION_REGEX = re.compile(r'^(?<!\\)\('
                                  r'(?P<text>.*?)'                 # full_text
                                  r'(?<!\\)\?(?P<fixedwidth>=?)'   # '?' or '?='
                                  r'(?P<value1>.+?)'               # first int/float
                                  r'(?P<operator>[<>=!]+)'         # operator
                                  r'(?P<value2>.+?)'               # second int/float
                                  # TODO: Add an optional 'else' separated by a ':'.
                                  r'(?<!\\)\)$')

    _CMP_OPS = { '<': operator.lt, '>': operator.gt,
                 '<=': operator.le, '>=': operator.ge,
                 '=': operator.eq, '!=': operator.ne }

    @classmethod
    def _apply_condition(cls, conditionstr):
        match = cls._CONDITION_REGEX.match(conditionstr)
        if match is None:
            raise ConditionError("Invalid condition: '{}'".format(conditionstr))
        else:
            op = match.group('operator')
            if op not in cls._CMP_OPS:
                raise ConditionError(("Invalid comparison operator in condition "
                                      "'{}': '{}'").format(conditionstr, op))
            else:
                op = cls._CMP_OPS[op]
                text = match.group('text')
                fixedwidth = match.group('fixedwidth')
                values = []
                for val in match.group('value1', 'value2'):
                    try:
                        values.append(str2num(val))
                    except ValueError:
                        raise ConditionError(("Non-number comparison in condition "
                                              "'{}': '{}'").format(conditionstr, val))

                if op(*values):
                    return text
                elif fixedwidth:
                    return ' '*len(text)
                else:
                    return ''


def unescape(string, chars=''):
    """Remove backslash in front of any character in `string` that is in `chars`"""
    if '\\' in string:
        for c in chars:
            string = string.replace('\\'+c, c)
    return string


class PrettyDict(abc.MutableMapping):
    """
    Dictionary that keeps raw and human-readable values

    Only raw values (e.g. 1000000) can be set. Those values are converted to a
    human-readable string (e.g. 'one million') when requested. This is done by
    passing raw values to user-supplied prettifier callables.

    >>> pd = PrettyDict(prettifiers={'percentage': lambda p: '{:.0f}%'.format(p*100)})
    >>> pd['percentage'] = 0.3412
    >>> pd['percentage']
    '34%'

    To get raw values, a '_' must be prepended to the key:

    >>> pd['_percentage']
    0.3412

    When setting values, it doesn't matter if there's a leading '_' or not.

    >>> pd['_percentage'] = 0.3412
    >>> pd['percentage']
    '34%'
    >>> pd['percentage'] = 34
    >>> pd['percentage']
    '3400%'

    If a key is not a string, the raw value is always returned.

    The default prettifier is `str`.
    """
    def __init__(self, prettifiers={}, **initial_values):
        self._prettifiers = prettifiers
        self._values_raw = {}
        self._values_pretty = {}
        self.update(initial_values)

    @property
    def prettifiers(self):
        """Dictionary that maps keys to callables"""
        return self._prettifiers

    @staticmethod
    def _real_key(key):
        """Strip the leading '_' if `key` is string'"""
        return key[1:] if isinstance(key, str) and key[0] is '_' else key

    def __setitem__(self, key, value):
        key = self._real_key(key)
        self._values_raw[key] = value
        self._invalidate(key)

    def _invalidate(self, key):
        """Forget prettification of `key`'s value"""
        if key in self._values_pretty:
            del self._values_pretty[key]

    def __getitem__(self, key):
        return_raw_value = not isinstance(key, str) or key[0] is '_'
        key = self._real_key(key)
        value = self._values_raw[key]
        if callable(value):
            value = value()
            self._invalidate(key)

        if return_raw_value:
            return value
        else:
            if key in self._values_pretty:
                # Use cached prettification
                return self._values_pretty[key]
            else:
                if key in self._prettifiers:
                    self._values_pretty[key] = self._prettifiers[key](value)
                else:
                    self._values_pretty[key] = str(value)
            return self._values_pretty[key]

    def __delitem__(self, item):
        key = self._real_key(item)
        del self._values_raw[key]
        if key in self._values_pretty:
            del self._values_pretty[key]

    def __iter__(self):
        keys_pretty = self._values_raw.keys()
        keys_raw = ('_'+key for key in keys_pretty)
        return (k for pair in zip(keys_pretty, keys_raw)
                for k in pair)

    def __len__(self):
        return len(tuple(iter(self)))

    def __repr__(self):
        items = []
        for k,v in self._values_raw.items():
            raw_val = v() if callable(v) else v
            items.append('{}={}={}'.format(k, raw_val, repr(self[k])))
        return '<{} {}>'.format(type(self).__name__, ', '.join(items))
