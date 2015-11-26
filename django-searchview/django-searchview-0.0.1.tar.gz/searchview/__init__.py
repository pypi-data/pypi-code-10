# -*- coding: utf-8 -*-

from .forms import SearchForm, searchform_factory
from .views import SearchView

VERSION = '0.0.1'

__all__ = [
    'SearchForm',
    'searchform_factory',
    'SearchView',
]
