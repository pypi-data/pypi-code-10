from django.test import override_settings

from parent_swap.tests.simple_app import models

from .utils import AppReloadTestCase


class TestSimpleObject(AppReloadTestCase):
    """
    Tests swappable BaseClass unconfigured: django.db.models.Model
    """
    def test_base(self):
        bases = models.SimpleObject.__bases__
        self.assertEqual(len(bases), 1)
        base_model = bases[0]
        self.assertEqual(base_model.__name__, 'Model')

    def test_create(self):
        simple = models.SimpleObject.objects.create(foo='hey hey hey')
        simple.save()
        self.assertTrue(models.SimpleObject.objects.filter(id=simple.id))


@override_settings(DEFAULT_BASE_CLASS='parent_swap.tests.parent_app.models.SimpleParent')
class TestConfiguredBaseClass(AppReloadTestCase):
    """
    Tests swappable BaseClass configured: SimpleParent
    """
    def test_base(self):
        bases = models.SimpleObject.__bases__
        self.assertEqual(len(bases), 1)
        base_model = bases[0]
        self.assertEqual(base_model.__name__, 'SimpleParent')

    def test_create(self):
        simple = models.SimpleObject.objects.create(foo='hey hey hey', bar='no no no')
        simple.save()
        self.assertTrue(models.SimpleObject.objects.filter(id=simple.id))
