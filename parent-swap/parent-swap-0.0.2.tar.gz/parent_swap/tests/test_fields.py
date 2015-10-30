from django.db import models
from django.test import override_settings

from parent_swap.tests.parent_app.models import SimpleParent

from .utils import AppReloadTestCase
from ..fields import (
    get_app_reference, get_cls_ptr, get_default_swap_field, get_swap_field,
    get_one_to_one_field_config
)


class TestMigrationSwap(AppReloadTestCase):

    def test_get_cls_ptr(self):
        ptr = get_cls_ptr(SimpleParent)
        self.assertEquals(ptr, 'simpleparent_ptr')

    def test_get_cls_ptr_string(self):
        ptr = get_cls_ptr('parent_swap.tests.parent_app.models.SimpleParent')
        self.assertEquals(ptr, 'simpleparent_ptr')

    def test_get_app_reference(self):
        ref = get_app_reference(SimpleParent)
        self.assertEqual(ref, 'parent_app.SimpleParent')

    def test_get_one_to_one_field_config(self):
        field = get_one_to_one_field_config(SimpleParent)
        expected_field = models.OneToOneField(
            parent_link=True,
            auto_created=True,
            primary_key=True,
            serialize=False,
            to='parent_app.SimpleParent'
        )
        self.assertEqual(field.auto_created, expected_field.auto_created)
        self.assertEqual(field.primary_key, expected_field.primary_key)
        self.assertEqual(field.serialize, expected_field.serialize)
        self.assertEqual(field.related_model, 'parent_app.SimpleParent')

    def test_get_one_to_one_field_config_str(self):
        field = get_one_to_one_field_config('parent_swap.tests.parent_app.models.SimpleParent')
        expected_field = models.OneToOneField(
            parent_link=True,
            auto_created=True,
            primary_key=True,
            serialize=False,
            to='parent_app.SimpleParent'
        )
        self.assertEqual(field.auto_created, expected_field.auto_created)
        self.assertEqual(field.primary_key, expected_field.primary_key)
        self.assertEqual(field.serialize, expected_field.serialize)
        self.assertEqual(field.related_model, 'parent_app.SimpleParent')

    def test_get_swap_field(self):
        ptr_name, onetoone = get_swap_field(SimpleParent)
        self.assertEqual(ptr_name, 'simpleparent_ptr')
        self.assertTrue(onetoone.auto_created)
        self.assertTrue(onetoone.primary_key)
        self.assertFalse(onetoone.serialize)
        self.assertEqual(onetoone.related_model, 'parent_app.SimpleParent')

    def test_get_swap_field_str(self):
        ptr_name, onetoone = get_swap_field('parent_swap.tests.parent_app.models.SimpleParent')
        self.assertEqual(ptr_name, 'simpleparent_ptr')
        self.assertTrue(onetoone.auto_created)
        self.assertTrue(onetoone.primary_key)
        self.assertFalse(onetoone.serialize)
        self.assertEqual(onetoone.related_model, 'parent_app.SimpleParent')

    def test_get_swap_field_django_model(self):
        ptr_name, field = get_swap_field(models.Model)
        self.assertEqual(ptr_name, 'id')
        self.assertEqual(field.verbose_name, 'ID')
        self.assertFalse(field.serialize)
        self.assertTrue(field.auto_created)
        self.assertTrue(field.primary_key)

    def get_default_swap_field_django_model(self):
        ptr_name, field = get_default_swap_field()
        self.assertEqual(ptr_name, 'id')
        self.assertEqual(field.verbose_name, 'ID')
        self.assertFalse(field.serialize)
        self.assertTrue(field.auto_created)
        self.assertTrue(field.primary_key)


@override_settings(DEFAULT_BASE_CLASS='parent_swap.tests.parent_app.models.SimpleParent')
class TestMigrationSwapDefaultBaseClassTestCase(AppReloadTestCase):
    """
    A bit excessive, but I want to teardown the app and retest the default field.
    """

    def test_get_default_swap_field_configured(self):
        ptr_name, field = get_default_swap_field()
        self.assertEqual(ptr_name, 'simpleparent_ptr')
        self.assertTrue(field.auto_created)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.serialize)
        self.assertEqual(field.related_model, 'parent_app.SimpleParent')
