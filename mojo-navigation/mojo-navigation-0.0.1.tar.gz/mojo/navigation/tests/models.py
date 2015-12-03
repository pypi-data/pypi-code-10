# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from mojo.navigation.models import ItemBase


class TestItem(ItemBase):
    def get_absolute_url(self):
        return reverse('mojo_navigation_tests_item', args=[self.pk])
