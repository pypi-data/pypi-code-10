# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

from leonardo.widgets import Widget


class CookieLawWidget(Widget):

    class Meta:
        abstract = True
        verbose_name = _("Cookie Law")
        verbose_name_plural = _("Cookie Law")
