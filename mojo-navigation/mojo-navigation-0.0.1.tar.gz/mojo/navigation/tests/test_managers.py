# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from mojo.navigation.tests.models import TestItem


class ItemManagerTest(TestCase):
    """
    Tests for mojo.navigation.managers.ItemManager
    """

    def setUp(self):
        # create a dummy user
        self.user = User(username=u"test", password="123")
        self.user.save()

        # create dummy group and permission
        self.group = Group(name=u"test group")
        self.group.save()
        self.permission = Permission.objects.get(pk=1)

        # create a tree item
        self.item = TestItem(parent=None, name=u"Test item")
        self.item.save()

    def test_for_slug_returns_only_tree_descendants(self):
        """
        Testing if the for_slug method, only returns the item descendants.
        """
        item_child = TestItem(parent=self.item, name=u"Test item child")
        item_child.save()
        item_child_child = TestItem(parent=item_child, name=u"Test item child child")
        item_child_child.save()
        items = TestItem.objects.for_slug(item_child.slug)
        self.assertNotIn(self.item, items)
        self.assertIn(item_child, items)
        self.assertIn(item_child_child, items)

    def test_for_user_superuser_accesses_all_items(self):
        """
        Testing if the user has access to any item even if he doesnt have to permission or group.
        """
        user = self.user
        self.item.access_permissions.add(self.permission)
        user.user_permissions.clear()
        user.is_superuser = True
        items = TestItem.objects.for_user(user)
        self.assertIn(self.item, items)
        self.item.access_permissions.clear()

    def test_for_user_loggedin_user_access(self):
        """
        Testing if a user can or not access an item if its restricted to logged in users and depending on the user
        login status.
        """
        user = self.user
        user.is_active = False
        self.item.access_loggedin = True
        self.item.save()
        items = TestItem.objects.for_user(user)
        self.assertNotIn(self.item, items)
        user.is_active = True
        items = TestItem.objects.for_user(user)
        self.assertIn(self.item, items)
        self.item.access_loggedin = False
        self.item.save()

    def test_for_user_permissions_restrictions(self):
        """
        Testing if the user has access to an item depending on permissions.
        """
        user = self.user
        self.item.access_permissions.add(self.permission)
        user.user_permissions.add(self.permission)
        items = TestItem.objects.for_user(user)
        self.assertIn(self.item, items)
        user.user_permissions.clear()
        items = TestItem.objects.for_user(user)
        self.assertNotIn(self.item, items)
        self.item.access_permissions.clear()

    def test_for_user_group_restrictions(self):
        """
        Testing if the user has access to an item depending on groups.
        """
        user = self.user
        self.item.access_group.add(self.group)
        user.groups.clear()
        items = TestItem.objects.for_user(user)
        self.assertNotIn(self.item, items)
        user.groups.add(self.group)
        items = TestItem.objects.for_user(user)
        self.assertIn(self.item, items)
        self.item.access_group.clear()

    def test_for_user_group_permissions_restrictions(self):
        """
        Testing if the user has access to an item depending on permissions set specificaly for a group.
        """
        user = self.user
        group = self.group
        self.item.access_permissions.add(self.permission)
        user.groups.add(group)
        items = TestItem.objects.for_user(user)
        self.assertNotIn(self.item, items)
        group.permissions.add(self.permission)
        items = TestItem.objects.for_user(user)
        self.assertIn(self.item, items)
        self.item.access_permissions.clear()
