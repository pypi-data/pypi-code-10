"""This sub-module provides 'keyboard awareness'."""

# std imports
import curses.has_key
import curses
import time
import re

# 3rd party
import six

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 requires 3rd party library (backport)
    #
    # pylint: disable=import-error
    #         Unable to import 'ordereddict'
    from ordereddict import OrderedDict


class Keystroke(six.text_type):
    """
    A unicode-derived class for describing a single keystroke.

    A class instance describes a single keystroke received on input,
    which may contain multiple characters as a multibyte sequence,
    which is indicated by properties :attr:`is_sequence` returning
    ``True``.

    When the string is a known sequence, :attr:`code` matches terminal
    class attributes for comparison, such as ``term.KEY_LEFT``.

    The string-name of the sequence, such as ``u'KEY_LEFT'`` is accessed
    by property :attr:`name`, and is used by the :meth:`__repr__` method
    to display a human-readable form of the Keystroke this class
    instance represents. It may otherwise by joined, split, or evaluated
    just as as any other unicode string.
    """

    def __new__(cls, ucs='', code=None, name=None):
        """Class constructor."""
        new = six.text_type.__new__(cls, ucs)
        new._name = name
        new._code = code
        return new

    @property
    def is_sequence(self):
        """Whether the value represents a multibyte sequence (bool)."""
        return self._code is not None

    def __repr__(self):
        """Docstring overwritten."""
        return (self._name is None and
                six.text_type.__repr__(self) or
                self._name)
    __repr__.__doc__ = six.text_type.__doc__

    @property
    def name(self):
        """String-name of key sequence, such as ``u'KEY_LEFT'`` (str)."""
        return self._name

    @property
    def code(self):
        """Integer keycode value of multibyte sequence (int)."""
        return self._code


def get_curses_keycodes():
    """
    Return mapping of curses key-names paired by their keycode integer value.

    :rtype: dict

    Returns dictionary of (name, code) pairs for curses keyboard constant
    values and their mnemonic name. Such as code ``260``, with the value of
    its key-name identity, ``u'KEY_LEFT'``.
    """
    _keynames = [attr for attr in dir(curses)
                 if attr.startswith('KEY_')]
    return dict(
        [(keyname, getattr(curses, keyname))
         for keyname in _keynames])


def get_keyboard_codes():
    """
    Return mapping of keycode integer values paired by their curses key-name.

    :rtype: dict

    Returns dictionary of (code, name) pairs for curses keyboard constant
    values and their mnemonic name. Such as key ``260``, with the value of
    its identity, ``u'KEY_LEFT'``.  These are derived from the attributes by
    the same of the curses module, with the following exceptions:

    * ``KEY_DELETE`` in place of ``KEY_DC``
    * ``KEY_INSERT`` in place of ``KEY_IC``
    * ``KEY_PGUP`` in place of ``KEY_PPAGE``
    * ``KEY_PGDOWN`` in place of ``KEY_NPAGE``
    * ``KEY_ESCAPE`` in place of ``KEY_EXIT``
    * ``KEY_SUP`` in place of ``KEY_SR``
    * ``KEY_SDOWN`` in place of ``KEY_SF``

    This function is the inverse of :func:`get_curses_keycodes`.  With the
    given override "mixins" listed above, the keycode for the delete key will
    map to our imaginary ``KEY_DELETE`` mnemonic, effectively erasing the
    phrase ``KEY_DC`` from our code vocabulary for anyone that wishes to use
    the return value to determine the key-name by keycode.
    """
    keycodes = OrderedDict(get_curses_keycodes())
    keycodes.update(CURSES_KEYCODE_OVERRIDE_MIXIN)

    # invert dictionary (key, values) => (values, key), preferring the
    # last-most inserted value ('KEY_DELETE' over 'KEY_DC').
    return dict(zip(keycodes.values(), keycodes.keys()))


def _alternative_left_right(term):
    r"""
    Determine and return mapping of left and right arrow keys sequences.

    :arg blessed.Terminal term: :class:`~.Terminal` instance.
    :rtype: dict

    This function supports :func:`get_terminal_sequences` to discover
    the preferred input sequence for the left and right application keys.

    Return dict of sequences ``term._cuf1``, and ``term._cub1``,
    valued as ``KEY_RIGHT``, ``KEY_LEFT`` (when appropriate).  It is
    necessary to check the value of these sequences to ensure we do not
    use ``u' '`` and ``u'\b'`` for ``KEY_RIGHT`` and ``KEY_LEFT``,
    preferring their true application key sequence, instead.
    """
    keymap = dict()
    if term._cuf1 and term._cuf1 != u' ':
        keymap[term._cuf1] = curses.KEY_RIGHT
    if term._cub1 and term._cub1 != u'\b':
        keymap[term._cub1] = curses.KEY_LEFT
    return keymap


def get_keyboard_sequences(term):
    r"""
    Return mapping of keyboard sequences paired by keycodes.

    :arg blessed.Terminal term: :class:`~.Terminal` instance.
    :returns: mapping of keyboard unicode sequences paired by keycodes
        as integer.  This is used as the argument ``mapper`` to
        the supporting function :func:`resolve_sequence`.
    :rtype: OrderedDict

    Initialize and return a keyboard map and sequence lookup table,
    (sequence, keycode) from :class:`~.Terminal` instance ``term``,
    where ``sequence`` is a multibyte input sequence of unicode
    characters, such as ``u'\x1b[D'``, and ``keycode`` is an integer
    value, matching curses constant such as term.KEY_LEFT.

    The return value is an OrderedDict instance, with their keys
    sorted longest-first.
    """
    # A small gem from curses.has_key that makes this all possible,
    # _capability_names: a lookup table of terminal capability names for
    # keyboard sequences (fe. kcub1, key_left), keyed by the values of
    # constants found beginning with KEY_ in the main curses module
    # (such as KEY_LEFT).
    #
    # latin1 encoding is used so that bytes in 8-bit range of 127-255
    # have equivalent chr() and unichr() values, so that the sequence
    # of a kermit or avatar terminal, for example, remains unchanged
    # in its byte sequence values even when represented by unicode.
    #
    capability_names = curses.has_key._capability_names
    sequence_map = dict((
        (seq.decode('latin1'), val)
        for (seq, val) in (
            (curses.tigetstr(cap), val)
            for (val, cap) in capability_names.items()
        ) if seq
    ) if term.does_styling else ())

    sequence_map.update(_alternative_left_right(term))
    sequence_map.update(DEFAULT_SEQUENCE_MIXIN)

    # This is for fast lookup matching of sequences, preferring
    # full-length sequence such as ('\x1b[D', KEY_LEFT)
    # over simple sequences such as ('\x1b', KEY_EXIT).
    return OrderedDict((
        (seq, sequence_map[seq]) for seq in sorted(
            sequence_map.keys(), key=len, reverse=True)))


def get_leading_prefixes(sequences):
    """
    Return a set of proper prefixes for given sequence of strings.

    :arg iterable sequences
    :rtype: set

    Given an iterable of strings, all textparts leading up to the final
    string is returned as a unique set.  This function supports the
    :meth:`~.Terminal.inkey` method by determining whether the given
    input is a sequence that **may** lead to a final matching pattern.

    >>> prefixes(['abc', 'abdf', 'e', 'jkl'])
    set([u'a', u'ab', u'abd', u'j', u'jk'])
    """
    return set(seq[:i] for seq in sequences for i in range(1, len(seq)))


def resolve_sequence(text, mapper, codes):
    r"""
    Return :class:`Keystroke` instance for given sequence ``text``.

    The given ``text`` may extend beyond a matching sequence, such as
    ``u\x1b[Dxxx`` returns a :class:`Keystroke` instance of attribute
    :attr:`Keystroke.sequence` valued only ``u\x1b[D``.  It is up to
    determine that ``xxx`` remains unresolved.

    :arg text: string of characters received from terminal input stream.
    :arg OrderedDict mapper: unicode multibyte sequences, such as ``u'\x1b[D'``
        paired by their integer value (260)
    :arg dict codes: a :type:`dict` of integer values (such as 260) paired
        by their mnemonic name, such as ``'KEY_LEFT'``.
    :rtype: Keystroke
    """
    for sequence, code in mapper.items():
        if text.startswith(sequence):
            return Keystroke(ucs=sequence, code=code, name=codes[code])
    return Keystroke(ucs=text and text[0] or u'')


def _time_left(stime, timeout):
    """
    Return time remaining since ``stime`` before given ``timeout``.

    This function assists determining the value of ``timeout`` for
    class method :meth:`~.Terminal.kbhit` and similar functions.

    :arg float stime: starting time for measurement
    :arg float timeout: timeout period, may be set to None to
       indicate no timeout (where None is always returned).
    :rtype: float or int
    :returns: time remaining as float. If no time is remaining,
       then the integer ``0`` is returned.
    """
    if timeout is not None:
        if timeout == 0:
            return 0
        return max(0, timeout - (time.time() - stime))


def _read_until(term, pattern, timeout):
    """
    Convenience read-until-pattern function, supporting :meth:`~.get_location`.

    :arg blessed.Terminal term: :class:`~.Terminal` instance.
    :arg float timeout: timeout period, may be set to None to indicate no
        timeout (where 0 is always returned).
    :arg str pattern: target regular expression pattern to seek.
    :rtype: tuple
    :returns: tuple in form of ``(match, str)``, *match*
        may be :class:`re.MatchObject` if pattern is discovered
        in input stream before timeout has elapsed, otherwise
        None. ``str`` is any remaining text received exclusive
        of the matching pattern).

    The reason a tuple containing non-matching data is returned, is that the
    consumer should push such data back into the input buffer by
    :meth:`~.Terminal.ungetch` if any was received.

    For example, when a user is performing rapid input keystrokes while its
    terminal emulator surreptitiously responds to this in-band sequence, we
    must ensure any such keyboard data is well-received by the next call to
    term.inkey() without delay.
    """
    stime = time.time()
    match, buf = None, u''

    # first, buffer all pending data. pexpect library provides a
    # 'searchwindowsize' attribute that limits this memory region.  We're not
    # concerned about OOM conditions: only (human) keyboard input and terminal
    # response sequences are expected.

    while True:
        # block as long as necessary to ensure at least one character is
        # received on input or remaining timeout has elapsed.
        ucs = term.inkey(timeout=_time_left(stime, timeout))
        if ucs:
            buf += ucs
            # while the keyboard buffer is "hot" (has input), we continue to
            # aggregate all awaiting data.  We do this to ensure slow I/O
            # calls do not unnecessarily give up within the first 'while' loop
            # for short timeout periods.
            while True:
                ucs = term.inkey(timeout=0)
                if not ucs:
                    break
                buf += ucs

        match = re.search(pattern=pattern, string=buf)
        if match is not None:
            # match
            break

        if timeout is not None:
            if not _time_left(stime, timeout):
                # timeout
                break

    return match, buf


def _inject_curses_keynames():
    r"""
    Inject KEY_NAMES that we think would be useful into the curses module.

    This function compliments the global constant
    :obj:`DEFAULT_SEQUENCE_MIXIN`.  It is important to note that this
    function has the side-effect of **injecting** new attributes to the
    curses module, and is called from the global namespace at time of
    import.

    Though we may determine *keynames* and codes for keyboard input that
    generate multibyte sequences, it is also especially useful to aliases
    a few basic ASCII characters such as ``KEY_TAB`` instead of ``u'\t'`` for
    uniformity.

    Furthermore, many key-names for application keys enabled only by context
    manager :meth:`~.Terminal.keypad` are surprisingly absent.  We inject them
    here directly into the curses module.

    It is not necessary to directly "monkeypatch" the curses module to
    contain these constants, as they will also be accessible as attributes
    of the Terminal class instance, they are provided only for convenience
    when mixed in with other curses code.
    """
    _lastval = max(get_curses_keycodes().values())
    for key in ('TAB', 'KP_MULTIPLY', 'KP_ADD', 'KP_SEPARATOR', 'KP_SUBTRACT',
                'KP_DECIMAL', 'KP_DIVIDE', 'KP_EQUAL', 'KP_0', 'KP_1', 'KP_2',
                'KP_3', 'KP_4', 'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9'):
        _lastval += 1
        setattr(curses, 'KEY_{0}'.format(key), _lastval)

_inject_curses_keynames()

#: In a perfect world, terminal emulators would always send exactly what
#: the terminfo(5) capability database plans for them, accordingly by the
#: value of the ``TERM`` name they declare.
#:
#: But this isn't a perfect world. Many vt220-derived terminals, such as
#: those declaring 'xterm', will continue to send vt220 codes instead of
#: their native-declared codes, for backwards-compatibility.
#:
#: This goes for many: rxvt, putty, iTerm.
#:
#: These "mixins" are used for *all* terminals, regardless of their type.
#:
#: Furthermore, curses does not provide sequences sent by the keypad,
#: at least, it does not provide a way to distinguish between keypad 0
#: and numeric 0.
DEFAULT_SEQUENCE_MIXIN = (
    # these common control characters (and 127, ctrl+'?') mapped to
    # an application key definition.
    (six.unichr(10), curses.KEY_ENTER),
    (six.unichr(13), curses.KEY_ENTER),
    (six.unichr(8), curses.KEY_BACKSPACE),
    (six.unichr(9), curses.KEY_TAB),
    (six.unichr(27), curses.KEY_EXIT),
    (six.unichr(127), curses.KEY_DC),

    (u"\x1b[A", curses.KEY_UP),
    (u"\x1b[B", curses.KEY_DOWN),
    (u"\x1b[C", curses.KEY_RIGHT),
    (u"\x1b[D", curses.KEY_LEFT),
    (u"\x1b[F", curses.KEY_END),
    (u"\x1b[H", curses.KEY_HOME),
    # not sure where these are from .. please report
    (u"\x1b[K", curses.KEY_END),
    (u"\x1b[U", curses.KEY_NPAGE),
    (u"\x1b[V", curses.KEY_PPAGE),

    # keys sent after term.smkx (keypad_xmit) is emitted, source:
    # http://www.xfree86.org/current/ctlseqs.html#PC-Style%20Function%20Keys
    # http://fossies.org/linux/rxvt/doc/rxvtRef.html#KeyCodes
    #
    # keypad, numlock on
    (u"\x1bOM", curses.KEY_ENTER),         # return
    (u"\x1bOj", curses.KEY_KP_MULTIPLY),   # *
    (u"\x1bOk", curses.KEY_KP_ADD),        # +
    (u"\x1bOl", curses.KEY_KP_SEPARATOR),  # ,
    (u"\x1bOm", curses.KEY_KP_SUBTRACT),   # -
    (u"\x1bOn", curses.KEY_KP_DECIMAL),    # .
    (u"\x1bOo", curses.KEY_KP_DIVIDE),     # /
    (u"\x1bOX", curses.KEY_KP_EQUAL),      # =
    (u"\x1bOp", curses.KEY_KP_0),          # 0
    (u"\x1bOq", curses.KEY_KP_1),          # 1
    (u"\x1bOr", curses.KEY_KP_2),          # 2
    (u"\x1bOs", curses.KEY_KP_3),          # 3
    (u"\x1bOt", curses.KEY_KP_4),          # 4
    (u"\x1bOu", curses.KEY_KP_5),          # 5
    (u"\x1bOv", curses.KEY_KP_6),          # 6
    (u"\x1bOw", curses.KEY_KP_7),          # 7
    (u"\x1bOx", curses.KEY_KP_8),          # 8
    (u"\x1bOy", curses.KEY_KP_9),          # 9

    # keypad, numlock off
    (u"\x1b[1~", curses.KEY_FIND),         # find
    (u"\x1b[2~", curses.KEY_IC),           # insert (0)
    (u"\x1b[3~", curses.KEY_DC),           # delete (.), "Execute"
    (u"\x1b[4~", curses.KEY_SELECT),       # select
    (u"\x1b[5~", curses.KEY_PPAGE),        # pgup   (9)
    (u"\x1b[6~", curses.KEY_NPAGE),        # pgdown (3)
    (u"\x1b[7~", curses.KEY_HOME),         # home
    (u"\x1b[8~", curses.KEY_END),          # end
    (u"\x1b[OA", curses.KEY_UP),           # up     (8)
    (u"\x1b[OB", curses.KEY_DOWN),         # down   (2)
    (u"\x1b[OC", curses.KEY_RIGHT),        # right  (6)
    (u"\x1b[OD", curses.KEY_LEFT),         # left   (4)
    (u"\x1b[OF", curses.KEY_END),          # end    (1)
    (u"\x1b[OH", curses.KEY_HOME),         # home   (7)

    # The vt220 placed F1-F4 above the keypad, in place of actual
    # F1-F4 were local functions (hold screen, print screen,
    # set up, data/talk, break).
    (u"\x1bOP", curses.KEY_F1),
    (u"\x1bOQ", curses.KEY_F2),
    (u"\x1bOR", curses.KEY_F3),
    (u"\x1bOS", curses.KEY_F4),
)

#: Override mixins for a few curses constants with easier
#: mnemonics: there may only be a 1:1 mapping when only a
#: keycode (int) is given, where these phrases are preferred.
CURSES_KEYCODE_OVERRIDE_MIXIN = (
    ('KEY_DELETE', curses.KEY_DC),
    ('KEY_INSERT', curses.KEY_IC),
    ('KEY_PGUP', curses.KEY_PPAGE),
    ('KEY_PGDOWN', curses.KEY_NPAGE),
    ('KEY_ESCAPE', curses.KEY_EXIT),
    ('KEY_SUP', curses.KEY_SR),
    ('KEY_SDOWN', curses.KEY_SF),
    ('KEY_UP_LEFT', curses.KEY_A1),
    ('KEY_UP_RIGHT', curses.KEY_A3),
    ('KEY_CENTER', curses.KEY_B2),
    ('KEY_BEGIN', curses.KEY_BEG),
)

__all__ = ('Keystroke', 'get_keyboard_codes', 'get_keyboard_sequences',)
