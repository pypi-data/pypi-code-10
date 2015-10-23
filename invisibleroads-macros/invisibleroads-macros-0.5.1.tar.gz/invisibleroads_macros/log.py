import re
from collections import OrderedDict
from os.path import expanduser


def sort_dictionary(value_by_key, sorted_keys):
    d = OrderedDict()
    for key in sorted_keys:
        try:
            d[key] = value_by_key[key]
        except KeyError:
            pass
    return d


def stylize_dictionary(value_by_key, suffix_format_packs):
    d = {}
    for key, value in value_by_key.iteritems():
        for suffix, format_value in suffix_format_packs:
            if key.endswith(suffix):
                value = format_value(value)
                break
        d[key] = value
    return d


def format_nested_dictionary(
        value_by_key, suffix_format_packs=None, prefix='', censored=False):
    parts = []
    if censored:
        value_by_key = OrderedDict(
            x for x in value_by_key.iteritems() if not x[0].startswith('_'))
    for key, value in value_by_key.iteritems():
        left_hand_side = prefix + str(key)
        if isinstance(value, dict):
            parts.append(format_nested_dictionary(
                value, suffix_format_packs, left_hand_side + '.'))
            continue
        for suffix, format_value in suffix_format_packs or []:
            if key.endswith(suffix):
                parts.append(left_hand_side + ' = ' + format_value(value))
                break
        else:
            if isinstance(value, basestring) and '\n' in value:
                text = format_indented_block(value)
                parts.append(left_hand_side + ' = ' + text)
            else:
                parts.append(left_hand_side + ' = ' + str(value))
    return '\n'.join(parts)


def format_path(x):
    return re.sub(r'^' + expanduser('~'), '~', x)


def format_hanging_indent(x):
    lines = x.strip().splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    return lines[0] + '\n' + '\n'.join('  ' + line for line in lines[1:])


def format_indented_block(x):
    return '\n' + '\n'.join('  ' + line for line in x.strip().splitlines())


def get_nested_dictionary(nested_lists):
    d = OrderedDict()
    for k, v in nested_lists:
        if k.endswith('_'):
            try:
                v = get_nested_dictionary(v)
            except TypeError:
                pass
            else:
                k = k[:-1]
        d[k] = v
    return d


def get_nested_lists(nested_dictionary):
    xs = []
    for k, v in nested_dictionary.iteritems():
        if hasattr(v, 'iteritems'):
            v = get_nested_lists(v)
            k = k + '_'
        xs.append((k, v))
    return xs


def parse_nested_dictionary(text, suffix_parse_packs=None):
    raw_dictionary, key = OrderedDict(), None
    for line in text.splitlines():
        if line.startswith('  '):
            if key is not None:
                value = line[2:].rstrip()
                raw_dictionary[key].append(value)
            continue
        try:
            key, value = line.split('=', 1)
        except ValueError:
            key = None
        else:
            key = key.strip()
            value = value.strip()
            raw_dictionary[key] = [value]
    d = OrderedDict()
    for k, v in raw_dictionary.iteritems():
        v = '\n'.join(v).strip()
        for suffix, parse_value in suffix_parse_packs or []:
            if k.endswith(suffix):
                v = parse_value(v)
        _set_nested_value(d, k, v)
    return d


def _set_nested_value(target_dictionary, key_string, value):
    this_dictionary = target_dictionary
    for key in key_string.split('.'):
        key = key.strip()
        last_dictionary = this_dictionary
        try:
            this_dictionary = this_dictionary[key]
        except KeyError:
            this_dictionary[key] = {}
            this_dictionary = this_dictionary[key]
    last_dictionary[key] = value
    return target_dictionary
