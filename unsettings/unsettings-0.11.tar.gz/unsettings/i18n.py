#-*- coding: utf-8-*-

import gettext, locale
from gettext import gettext as _

import settings

gettext.bindtextdomain(settings.GETTEXT_DOMAIN, settings.LOCALE_DIR)
gettext.textdomain(settings.GETTEXT_DOMAIN)
try:
    locale.setlocale(locale.LC_ALL, "")
    # we need this for bug #846038, with en_NG setlocale() is fine
    # but the next getlocale() will crash (fun!)
    locale.getlocale()
except:
    locale.setlocale(locale.LC_ALL, "C")

