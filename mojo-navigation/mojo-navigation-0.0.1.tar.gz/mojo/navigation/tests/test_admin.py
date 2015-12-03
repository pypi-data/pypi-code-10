# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory

from mojo.navigation.admin import ItemAdmin
from mojo.navigation.tests.models import TestItem


class MockRequest(object):
    pass


class MockSuperUser(object):
    is_active = True
    is_staff = True

    def has_perm(self, perm):
        return True  # pragma: no cover

request = RequestFactory()
request.user = MockSuperUser()
request.csrf_processing_done = True


class ItemAdminTest(TestCase):
    """
    Tests for mojo.navigation.admin.ItemAdmin
    """

    def setUp(self):
        # create a menu parent
        self.menu_parent = TestItem(name=u"Parent")
        self.menu_parent.save()

        # create a menu child
        self.menu_child = TestItem(parent=self.menu_parent, name=u"Child")
        self.menu_child.save()

        # create a site instance
        self.site = AdminSite()

    def test_level_limit_filters_parent_queryset_levels(self):
        """
        Testing if level_limit is set the parent field queryset should filter and remove levels underneath.
        """
        # if no level_limit, all levels are returned.
        item_admin = ItemAdmin(TestItem, self.site)
        form = item_admin.get_form(request)
        queryset = form.base_fields['parent']._queryset
        self.assertEqual(len(queryset), 2)
        self.assertIn(self.menu_parent, queryset)
        self.assertIn(self.menu_child, queryset)
        # if level_limit=1, the root level items should be removed.
        item_admin = ItemAdmin(TestItem, self.site)
        item_admin.level_limit = 1
        form = item_admin.get_form(request)
        queryset = form.base_fields['parent']._queryset
        self.assertEqual(len(form.base_fields['parent']._queryset), 1)
        self.assertNotIn(self.menu_child, queryset)
