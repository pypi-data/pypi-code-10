import collections
import contextlib
import gettext as gnu
import os
import threading
import re


LOCALE_PATTERN = re.compile('^(?P<lang>[a-z]{2})_[A-Z]{2}$')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE')
_active = threading.local()
_translations = collections.defaultdict(dict)
_default = None
_domain = None


def load(domain, localedir, **kwargs):
    global _default
    global DEFAULT_LANGUAGE

    is_default = kwargs.pop('is_default', False)
    languages = kwargs.pop('languages', [])
    t = gnu.translation(domain, localedir, languages=languages)
    for lang in languages:
        _translations[domain][lang] = t

    if is_default:
        _default = t
        DEFAULT_LANGUAGE = t.info()['language']


@contextlib.contextmanager
def language(language_code, fatal=False):
    """Return a context guard that activates a certain language
    and deactivates it when exiting.
    """
    current = activate(language_code)
    yield
    activate(current)


def activate(lang):
    """Sets the current active language to `lang`."""
    current = getattr(_active, 'value', None)
    _active.value = lang
    return current


def get_language():
    """Return a string indicating the currently activated
    language.
    """
    return getattr(_active, 'value', DEFAULT_LANGUAGE)


def dgettext(domain, *args, **kwargs):
    """Like :func:`gettext()`, but look the message up in specified
    `domain`.
    """
    lang = get_language()
    try:
        t = _get_translation(domain, lang)
        return t.gettext(*args, **kwargs)
    except KeyError:
        if _default is None:
            raise

        return _default.gettext(*args, **kwargs)


def _get_translation(domain, lang):
    # If the language code is not in the translations dictionary,
    # try to do some parsing.
    if lang not in _translations[domain]:
        m = LOCALE_PATTERN.match(lang)
        if m is None:
            raise KeyError(lang)
        lang = m.groupdict()['lang']
        return _get_translation(domain, lang)

    return _translations[domain][lang]
