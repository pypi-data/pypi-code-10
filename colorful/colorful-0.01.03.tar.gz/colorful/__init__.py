# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""
    Python module to colorize your console outputs.
"""

from sys import stdout

try:
    from colorama import init as init_ansi_colors_on_windows
    init_ansi_colors_on_windows()
except ImportError:
    pass


class ANSISequenceNotFoundError(Exception):
    """Error if an ANSI sequence could not be found"""
    def __init__(self, modetype, name):
        Exception.__init__(self, "ANSI Sequence `%s` could not be found in `%s`" % (name, modetype))


class ColorfulParser(object):
    """Colorful is a class to decorate text with ANSI colors and modifiers."""

    _modifiers = {
        "reset": 0,
        "bold": 1,
        "italic": 3,
        "underline": 4,
        "blink": 5,
        "inverse": 7,
        "strikethrough": 9
    }
    _forecolors = {
        "black": 30,
        "red": 31,
        "green": 32,
        "brown": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "normal": 39,
    }
    _backcolors = {
        "black": 40,
        "red": 41,
        "green": 42,
        "brown": 43,
        "blue": 44,
        "magenta": 45,
        "cyan": 46,
        "white": 47,
        "normal": 49,
    }

    _modifier_splitter = "and"
    _backcolor_splitter = "on"

    @classmethod
    def _get_ansi_decorator(cls, mode):
        """Returns the ANSI sequence for the given mode"""
        return "\033[%sm" % mode

    @classmethod
    def foreground_color_exists(cls, color):
        """Check if the given color is a valid foreground color"""
        return color in cls._forecolors

    @classmethod
    def background_color_exists(cls, color):
        """Check if the given color is a valid background color"""
        return color in cls._backcolors

    @classmethod
    def _translate_to_ansi_decorator(cls, modetype, name):
        """
            Translate the name of the modetype to a valid ANSI sequence
        """
        try:
            return cls._get_ansi_decorator(modetype[name])
        except KeyError:
            raise ANSISequenceNotFoundError(modetype.__class__.__name__, name)

    @classmethod
    def parse(cls, attr):
        """
            Parse the attr and decorate it with colors
        """
        parts = attr.split("_")

        modifiers = ""
        forecolor = ""
        backcolor = ""

        if parts[0] in cls._modifiers:
            modifiers += cls._translate_to_ansi_decorator(cls._modifiers, parts[0])
            parts = parts[1:]

        if cls._modifier_splitter in parts:
            for part in [parts[p + 1] if p + 1 < len(parts) else None for p in range(len(parts)) if parts[p] == cls._modifier_splitter]:
                modifiers += cls._translate_to_ansi_decorator(cls._modifiers, part)
            parts = parts[(len(parts) - parts[-1::-1].index(cls._modifier_splitter) - 1) + 2:]

        if "on" in parts:
            backcolor = cls._translate_to_ansi_decorator(cls._backcolors, parts[parts.index(cls._backcolor_splitter) + 1])
            parts = parts[:-2]

        if len(parts) > 0:
            forecolor = cls._translate_to_ansi_decorator(cls._forecolors, parts[0])

        return modifiers + forecolor + backcolor + "%s" + cls._translate_to_ansi_decorator(cls._modifiers, "reset")


class Colorful(object):  # pylint: disable=too-few-public-methods
    """
        Provides functionality to colorize your outputs.
    """
    class _Out(object):  # pylint: disable=too-few-public-methods
        """
            Write directly to stdout
        """
        def __getattr__(self, attr):
            def _decorated_text(text):
                """
                    Decorate the given text with colors
                """
                print(ColorfulParser.parse(attr) % text)  # pylint: disable=superfluous-parens
                stdout.flush()
            return _decorated_text

    out = _Out()

    def __getattr__(self, attr):
        """
            Gets the function to colorize your output.
        """
        def _decorated_text(text):
            """
                Decorate the given text with colors
            """
            return ColorfulParser.parse(attr) % text
        return _decorated_text


colorful = Colorful()  # pylint: disable=invalid-name
