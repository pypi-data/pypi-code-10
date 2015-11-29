# Released under GPL3 terms (see LICENSE file)

from . import validation
import re
import math
import json
import logging
import sys


class I3Stdout():
    """Wrapper for sys.stdout that optimizes printing to i3bar"""

    _initialized = False
    _HEADER = json.dumps({ 'version': 1, 'click_events': False }) + '\n[[],\n'

    def write(self, b):
        if not self._initialized:
            sys.__stdout__.write(self._HEADER)
            self._initialized = True
        sys.__stdout__.write(b)
        sys.__stdout__.flush()

    def __getattr__(self, name):
        return getattr(sys.__stdout__, name)


class I3Block():
    DEFAULTS = {
        'full_text': '',
    }

    VALIDATORS = {
        'align': lambda v: validation.validate_option(v, ('left', 'right', 'center')),
        'instance': lambda v: str(v),
        'markup': lambda v: validation.validate_option(v, ('pango', 'none')),
        'min_width': lambda v: validation.validate_integer(v, min=0),
        'name': lambda v: str(v),
        'separator': validation.validate_bool,
        'separator_block_width': lambda v: validation.validate_integer(v),
        'urgent': validation.validate_bool,

        # These need an instance and are therefore specified in __init__()
        'full_text': None,
        'short_text': None,
        'color': None,
    }

    VALID_FIELDS = tuple(VALIDATORS) + \
                   tuple('dyncolor_'+k for k in ('colors', 'value', 'min', 'max',
                                                 'softmin', 'softmax', 'scale'))

    REGEX_VBAR = re.compile(r'vbar(\S*?)\((.*?)\)')

    def __init__(self, **initial_vars):
        self._errors = []
        self._vbars = {}
        self._dyncolor = DynamicColor()
        self._use_dyncolor = False
        self._full_text_functions = [
            ('vbar', self.REGEX_VBAR, self._make_vbar)
            # TODO: Add more functions:
            #   - hbar(): horizontal bar
            #   - graph(): list of vertical bars that shift their values from
            #              right to left over time
        ]

        validators = self.VALIDATORS.copy()
        validators.update(full_text=self._parse_function_calls,
                          short_text=self._parse_function_calls,
                          color=self._parse_color)

        self._i3vars = validation.VDict(validators=validators,
                                        valid_keys=tuple(validators),
                                        **self.DEFAULTS)
        self.update(**initial_vars)

    def _parse_function_calls(self, text):
        for funcname,funcregex,func in self._full_text_functions:
            while True:
                match = funcregex.search(text)
                if match is None:
                    break
                callid = match.group(1)
                posargs = []
                kwargs = []
                for arg in (arg.strip() for arg in match.group(2).split(',')):
                    if '=' in arg:
                        kwargs.append(tuple(arg.split('=', 1)))
                    else:
                        posargs.append(arg)
                replacement = str(func(callid, posargs, kwargs))
                text = text[:match.start()] + replacement + text[match.end():]
        return text

    def _make_vbar(self, callid='', posargs=(), kwargs=()):
        posargnum = len(posargs)
        if posargnum > 1:
            self._errors.append('Too many positional vbar() arguments: {}'
                                .format(', '.join(posargs)))
            return '!'
        elif posargnum == 1:
            kwargs += (('value', posargs[0]),)
        try:
            if callid not in self._vbars:
                self._vbars[callid] = VerticalBar(*kwargs)
            else:
                self._vbars[callid].update(*kwargs)
        except (KeyError,ValueError) as e:
            self._errors.append('Invalid vbar() argument: {}'.format(e))
            return '!'
        else:
            return str(self._vbars[callid])

    @property
    def json(self):
        if self._use_dyncolor and bool(self._dyncolor):
            i3vars = dict(self._i3vars)
            i3vars['color'] = str(self._dyncolor)
            return json.dumps(i3vars)
        else:
            return json.dumps(self._i3vars)

    @property
    def errors(self):
        errors = list(self._errors)
        self._errors = []
        return errors

    def copy(self):
        copy = type(self)()
        copy.update(**self._i3vars)
        copy._dyncolor = self._dyncolor.copy()
        copy._vbars = dict((id,vbar.copy())
                           for id,vbar in self._vbars.items())
        return copy

    def update(self, **dct):
        if 'color' in dct and 'dyncolor_value' in dct:
            self._errors.append("Specifying both 'color' and 'dyncolor_value' is ambiguous.")
        else:
            for key,value in dct.items():
                try:
                    self[key] = value
                except Exception as e:
                    self._errors.append(e)

    def __setitem__(self, key, value):
        try:
            if key.startswith('dyncolor_'):
                arg_key = key[9:]  # Remove 'dyncolor_'
                self._dyncolor[arg_key] = value
                self._use_dyncolor = True
            else:
                self._i3vars[key] = value
                if key == 'color':
                    self._use_dyncolor = False
        except ValueError as e:
            self._errors.append('{}: {}'.format(key, e))
        except KeyError as key:
            self._errors.append('Invalid field: {}'.format(key))

    def __getitem__(self, key):
        if key == 'color' and self._use_dyncolor and bool(self._dyncolor):
            return str(self._dyncolor)
        try:
            return self._i3vars[key]
        except KeyError as key:
            self._errors.append('Invalid field: {}'.format(key))

    def __delitem__(self, key):
        try:
            del(self._i3vars[key])
        except KeyError as key:
            self._errors.append('Invalid field: {}'.format(key))

    def __contains__(self, key):
        return key in self._i3vars

    def __eq__(self, other):
        if isinstance(other, type(self)):
            for attr in ('_i3vars', '_dyncolor', '_vbars'):
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        else:
            return NotImplemented

    def __repr__(self):
        r = '<{} '.format(type(self).__name__)
        r += ', '.join('{}={!r}'.format(k, v)
                       for k,v in sorted(self._i3vars.items()))
        if self._dyncolor:
            r += ', ' + repr(self._dyncolor)
        return r+'>'

    def _parse_color(self, string):
        """
        Set 'color' value to static or dynamic color

        `string` is a list of parameters separated by ':'.

        Valid parameters are:
          - a list of RGB color codes, separated by '-'
          - a number (int/float, optionally prefixed by 'value=')
          - [min|max|softmin|softmax]=<number> (dyncolor's limits)
          - scale=[linear|sqrt|log]

        Specifying a color list creates a new DynamicColor object and discards
        the old one, including any cached value->color pairs.

        Example: #ff0000-#0f0-#0000ff:25:min=0:softmax=100
        """
        string = str(string)
        try:
            return str(RGBColor(string))
        except ValueError:
            for part in string.split(':'):
                if part == '':
                    continue

                try:
                    self._dyncolor['value'] = int(float(part))
                except ValueError:
                    if '=' in part:
                        key, val = part.split('=', 1)
                        self._dyncolor[key.lower()] = val
                    else:
                        self._dyncolor['colors'] = part
            return str(self._dyncolor)


class Ratio():
    """Relation of a changing number to minimum and maximum numbers"""

    SCALES = { 'linear': lambda v: v,
               'sqrt': math.sqrt,
               'log': math.log }

    def __init__(self, *settings):
        self._ratio = None
        self._value = None
        self._min = 0
        self._max = 0
        self.min_is_soft = True
        self.max_is_soft = True
        self._scalename = 'linear'
        self._scale = self.SCALES[self._scalename]
        self._recalc = True
        self.update(*settings)
        if self._value is None: self._value = self._min
        if self._ratio is None: self._ratio = float(0)

    def update(self, *settings):
        for k,v in settings:
            self[k] = v

    def __getitem__(self, item):
        if item == 'value': return self._value
        if item in ('min', 'softmin'): return self._min
        if item in ('max', 'softmax'): return self._max
        if item == 'scale': return self._scalename
        raise KeyError(item)

    def __setitem__(self, item, value):
        if item in ('value', 'min', 'max', 'softmin', 'softmax'):
            value = validation.validate_number(value)

        if item == 'value':
            if value < self._min:
                if self.min_is_soft:
                    self['softmin'] = value
                else:
                    value = self._min
            elif value > self._max:
                if self.max_is_soft:
                    self['softmax'] = value
                else:
                    value = self._max
            self._value = value

        elif item == 'min':
            self._min = value
            self.min_is_soft = False
        elif item == 'max':
            self._max = value
            self.max_is_soft = False

        elif item == 'softmin':
            self._min = value
            self.min_is_soft = True
        elif item == 'softmax':
            self._max = value
            self.max_is_soft = True

        elif item == 'scale':
            value = validation.validate_option(value, options=tuple(self.SCALES))
            self._scale = self.SCALES[value]
            self._scalename = value
        else:
            raise KeyError(item)

        self._recalc = True

    def __float__(self):
        """Return ratio as float between 0 and 1"""
        if self._recalc:
            abs_max = self._max - self._min
            abs_rel = self._value - self._min
            try:
                abs_max = self._scale(abs_max)
                abs_rel = self._scale(abs_rel)
            except ValueError:
                pass  # Ignoring 'math domain error' seems to work

            try:
                self._ratio = float(max(0, min(1, abs_rel/abs_max)))
            except ZeroDivisionError:
                self._ratio = float(0)

            self._recalc = False

        return self._ratio

    def __round__(self, n=0):
        return round(float(self), n)

    def __str__(self):
        return str(round(self, 3))

    @property
    def as_percent(self):
        return float(self) * 100

    def __int__(self):
        """Return ratio as int between 0 and 100"""
        return int(self.as_percent)

    def copy(self):
        settings = [('value', self._value), ('scale', self._scalename)]
        if self.min_is_soft:
            settings.append(('softmin', self._min))
        else:
            settings.append(('min', self._min))
        if self.max_is_soft:
            settings.append(('softmax', self._max))
        else:
            settings.append(('max', self._max))
        return type(self)(*settings)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            for key in ('value', 'min', 'max', 'scale'):
                if self[key] != other[key]:
                    return False
            for attr in ('min_is_soft', 'max_is_soft', '_ratio'):
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        elif isinstance(other, (int, float)):
            return self._ratio == other
        else:
            return NotImplemented

    def __repr__(self):
        r = '<{} {}->{}'.format(type(self).__name__, self._value, self._ratio)
        if self.min_is_soft:
            r += ', softmin={}'.format(self._min)
        else:
            r += ', min={}'.format(self._min)
        if self.max_is_soft:
            r += ', softmax={}'.format(self._max)
        else:
            r += ', max={}'.format(self._max)
        r += ', scale={}>'.format(self._scalename)
        return r


class RGBColor():
    """Mixable RGB color"""

    HEXCHARS = '0123456789abcdefABCDEF'

    def __init__(self, rgb):
        if not isinstance(rgb, str) or \
           len(rgb) not in (7, 4) or \
           not rgb.startswith('#') or \
           not all(c in self.HEXCHARS for c in rgb[1:]):
            raise ValueError('Invalid RGB color: {!r}'.format(rgb))
        rgb = rgb.lstrip('#')
        if len(rgb) == 3:
            # Convert 3-digit notation to 6-digit notation
            rgb = rgb[0]+rgb[0] + rgb[1]+rgb[1] + rgb[2]+rgb[2]
        self.r = int(rgb[0:2], 16)
        self.g = int(rgb[2:4], 16)
        self.b = int(rgb[4:6], 16)

    def combine(self, other, factor):
        cls_self = type(self)
        cls_other = type(other)
        if not cls_self == cls_other:
            raise ValueError('Cannot combine {!r} ({}) and {!r} ({})'
                             .format(self, cls_self.__name__,
                                     other, cls_other.__name__))
        rgb = '#'
        for col in ('r', 'g', 'b'):
            # I don't really understand the '* (256/255)' part, but the
            # maximum 0xff is 255, and fracturing that is "wrong" (255*0.5 is
            # 127.5, not 128 (0x80)), and what I'm doing here "elevates" all
            # values to a maximum of 256, even though they stay mostly the
            # same. (Also, I suck at math.)
            val_other = getattr(other, col) * (256/255)
            val_self = getattr(self, col) * (256/255)
            val_new = max(0, min(255, ((val_other*factor) + (val_self*(1-factor)))))
            rgb += '{:02X}'.format(round(val_new))
        return cls_self(rgb)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.r == other.r and
                    self.g == other.g and
                    self.b == other.b)
        else:
            # Maybe other is RGB string?
            try:
                other = type(self)(other)
            except:
                return False
            else:
                return repr(self) == repr(other)

    def __str__(self):
        return '#' + ''.join(['%02X' % c for c in (self.r, self.g, self.b)])

    __repr__ = __str__


class DynamicColor():
    """Create new RGB colors from a list of RGB colors based on Ratio"""

    def __init__(self, colors=(), settings=()):
        self._colors = ()
        self._color_num = 0
        self._max_color_index = -1
        self._ratio = Ratio()
        self._cache = {}
        self._current_color = ''
        self.update(colors, settings)

    def update(self, colors=(), settings=()):
        if colors:
            self['colors'] = colors
        try:
            for k,v in settings:
                self[k] = v
        except ValueError:
            raise ValueError('not an iterable of key-value pairs: {!r}'.format(settings))
        return str(self)

    def _mix_new_color(self, value):
        i_max = self._max_color_index
        if i_max < 0:
            self._current_color = ''
        else:
            # Find the two relevant colors
            if self._color_num == 2:
                color_min, color_max = self._colors
                i1, i2 = 0, 1
            else:
                fraction = value / 100
                i2 = min(i_max, round((i_max * fraction) + 0.50000001))
                i1 = i2-1
                color_min = self._colors[i1]
                color_max = self._colors[i2]

            # Figure out where value is between its limits
            value_min = 100 * ( float(i1) / i_max)
            value_max = 100 * ( float(i2) / i_max)
            factor = (value - value_min) / (value_max - value_min)

            # Combine the two colors
            self._current_color = str(color_min.combine(color_max, factor))
            self._cache[value] = self._current_color
        return self._current_color

    def __getitem__(self, item):
        if item == 'color':
            return self._current_color
        elif item == 'colors':
            return tuple(str(c) for c in self._colors)
        else:
            return self._ratio[item]

    def __setitem__(self, item, value):
        if item == 'colors':
            if not isinstance(value, (list, tuple, set)):
                value = value.split('-')
            value = tuple(value)
            if value != self._colors:
                new_colors = []
                for c in value:
                    if isinstance(c, RGBColor):
                        new_colors.append(c)
                    else:
                        new_colors.append(RGBColor(c.strip()))
                self._colors = tuple(new_colors)
                self._color_num = len(self._colors)
                self._max_color_index = self._color_num-1
                self._cache = {}
        else:
            self._ratio[item] = value

    def copy(self):
        copy = type(self)(colors=[str(c) for c in self._colors])
        copy._color_num = self._color_num
        copy._max_color_index = self._max_color_index
        copy._ratio = self._ratio.copy()
        copy._cache = self._cache.copy()
        copy._current_color = self._current_color
        return copy

    def __str__(self):
        if self._color_num < 1:
            self._current_color = ''
        elif self._color_num == 1:
            self._current_color = str(self._colors[0])
        else:
            value = int(self._ratio)
            try:
                self._current_color = self._cache[value]
            except KeyError:
                self._mix_new_color(value)
        return self._current_color

    def __repr__(self):
        r = '-'.join(str(c) for c in self._colors)
        if self._ratio['min'] != 0:
            if self._ratio.min_is_soft:
                r += ':softmin={}'.format(self._ratio['min'])
            else:
                r += ':min={}'.format(self._ratio['min'])
        if self._ratio['max'] != 0:
            if self._ratio.max_is_soft:
                r += ':softmax={}'.format(self._ratio['max'])
            else:
                r += ':max={}'.format(self._ratio['max'])
        r += ':{}'.format(self._ratio['value'])
        return r

    def __eq__(self, other):
        if isinstance(other, type(self)):
            for attr in ('_colors', '_ratio', '_current_color'):
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        else:
            return NotImplemented

    def __bool__(self):
        return str(self) != ''


class VerticalBar():
    """Use unicode characters to create a vertical bar"""

    CHARS = (' ', '\u2581', '\u2582', '\u2583', '\u2584',
             '\u2585', '\u2586', '\u2587', '\u2588')
    MAX_INDEX = len(CHARS)-1

    def __init__(self, *settings):
        self._ratio = Ratio(*settings)
        self._current_char = self._get_char()

    def update(self, *settings):
        self._ratio.update(*settings)
        self._current_char = self._get_char()
        return self._current_char

    def _get_char(self):
        index = round(self.MAX_INDEX * float(self._ratio))
        return self.CHARS[index]

    def copy(self):
        copy = type(self)()
        copy._ratio = self._ratio.copy()
        copy._current_char = self._current_char
        return copy

    def __str__(self):
        return self._current_char
