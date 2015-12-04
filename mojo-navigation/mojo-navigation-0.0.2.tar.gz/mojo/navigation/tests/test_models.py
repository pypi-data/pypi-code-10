# -*- coding: utf-8 -*-

from django.test import TestCase

from mojo.navigation.tests.models import TestItem


class ItemTest(TestCase):
    """
    Tests for mojo.navigation.models.MojoMenu
    """

    def setUp(self):
        self.item = TestItem(name=u"Test")

    def test_unicode_str_retun_object_name(self):
        """
        Testing if __str__ or __unicode__ return the Item object name.
        """
        self.assertEqual(self.item.__str__(), self.item.name)

    def test_url_is_valid_validation(self):
        """
        Testing if url_is_valid method triggers accurate result.
        """
        # when url is unset, False should be returned.
        self.item.url = ''
        self.assertFalse(self.item.url_is_valid())
        # when an invalid url is passed, False should be returned
        self.item.url = 'test.com'
        self.assertFalse(self.item.url_is_valid())
        self.item.url = '/test.com'
        self.assertFalse(self.item.url_is_valid())
        self.item.url = 'http://'
        self.assertFalse(self.item.url_is_valid())
        # when a valid url is passed, True should be returned
        self.item.url = 'http://test.com/test'
        self.assertTrue(self.item.url_is_valid())

    def test_url_is_pattern_validation(self):
        """
        Testing if url_is_pattern method triggers accurate result.
        """
        # when url is unset, False should be returned.
        self.item.url = ''
        self.assertFalse(self.item.url_is_pattern())
        # when an invalid url is passed, False should be returned
        self.item.url = 'http://test.com'
        self.assertFalse(self.item.url_is_pattern())
        # when a valid url is passed, True should be returned
        self.item.url = 'admin:auth_user_changelist'
        self.assertTrue(self.item.url_is_pattern())

    def test_setting_href_from_url(self):
        """
        Testing if the href field is properly set from the url field.
        """
        # when url is unset, href should not be set as well.
        self.item.url = ''
        self.item.save()
        self.assertEqual(self.item.href, '')
        # when an absolute url is set for url field href should take it.
        self.item.url = 'http://test.com'
        self.item.save()
        self.assertEqual(self.item.href, self.item.url)
        # when a django url pattern is set for url field href should be set to its path.
        self.item.url = 'admin:auth_user_changelist'
        self.item.save()
        self.assertEqual(self.item.href, '/admin/auth/user/')
        # when url field set to a relative, href take the same value.
        self.item.url = '/test'
        self.item.save()
        self.assertEqual(self.item.href, self.item.url)
        # when the url field is set and valid as well as content_object, href should prioritize url field.
        self.item.content_object = self.item
        self.item.save()
        self.assertEqual(self.item.href, self.item.url)
        # when the url field is not set or valid but content_object is set, href should be equal to the conten_object
        # get_absolute_url() value.
        self.item.url = ''
        self.item.save()
        self.assertEqual(self.item.href, self.item.get_absolute_url())

    def test_unique_slug_generated(self):
        """
        Testing if a unique slug is generated when saving.
        """
        self.item.save()
        self.assertNotEqual('', self.item.slug)
        new_item = TestItem(name=self.item.name)
        new_item.save()
        self.assertNotEqual(self.item.slug, new_item.slug)
        self.assertIn('-', new_item.slug)
