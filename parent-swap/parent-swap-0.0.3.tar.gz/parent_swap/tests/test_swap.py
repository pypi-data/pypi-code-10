from django.test import override_settings

from parent_swap.tests.simple_app import models
from parent_swap.tests.simple_app import serializers
from parent_swap.tests.simple_app import views

from .utils import AppReloadTestCase


OVERRIDE_SETTINGS = {
    'DEFAULT_BASE_MODEL': 'parent_swap.tests.parent_app.models.SimpleParent',
    'DEFAULT_SERIALIZER': 'parent_swap.tests.parent_app.serializers.SimpleParentSerializer',
    'DEFAULT_VIEW': 'parent_swap.tests.parent_app.views.SimpleParentDetailView'
}


class TestSimpleObject(AppReloadTestCase):
    """
    Tests swappable BaseModel unconfigured: django.db.models.Model
    """
    def test_base_model(self):
        bases = models.SimpleObject.__bases__
        self.assertEqual(len(bases), 1)
        base_model = bases[0]
        self.assertEqual(base_model.__name__, 'Model')

    def test_base_mapping(self):
        bases = models.SimpleObject.Mapping.__bases__
        self.assertEqual(len(bases), 1)
        base_mapping = bases[0]
        self.assertEqual(base_mapping.__name__, 'object')

    def test_base_serializer(self):
        bases = serializers.SimpleObjectSerializer.__bases__
        self.assertEqual(len(bases), 1)
        base_serializer = bases[0]
        self.assertEqual(base_serializer.__name__, 'Serializer')

    def test_base_view(self):
        bases = views.SimpleObjectDetailView.__bases__
        self.assertEqual(len(bases), 1)
        base_view = bases[0]
        self.assertEqual(base_view.__name__, 'DetailView')

    def test_create(self):
        simple = models.SimpleObject.objects.create(foo='hey hey hey')
        simple.save()
        self.assertTrue(models.SimpleObject.objects.filter(id=simple.id))


@override_settings(**OVERRIDE_SETTINGS)
class TestConfiguredBaseModel(AppReloadTestCase):
    """
    Tests swappable BaseModel configured: SimpleParent
    """
    def test_base_model(self):
        bases = models.SimpleObject.__bases__
        self.assertEqual(len(bases), 1)
        base_model = bases[0]
        self.assertEqual(base_model.__name__, 'SimpleParent')

    def test_base_mapping(self):
        bases = models.SimpleObject.Mapping.__bases__
        self.assertEqual(len(bases), 1)
        base_mapping = bases[0]
        self.assertEqual(base_mapping.__name__, 'Mapping')

    def test_base_serializer(self):
        bases = serializers.SimpleObjectSerializer.__bases__
        self.assertEqual(len(bases), 1)
        base_serializer = bases[0]
        self.assertEqual(base_serializer.__name__, 'SimpleParentSerializer')

    def test_base_view(self):
        bases = views.SimpleObjectDetailView.__bases__
        self.assertEqual(len(bases), 1)
        base_view = bases[0]
        self.assertEqual(base_view.__name__, 'SimpleParentDetailView')

    def test_create(self):
        simple = models.SimpleObject.objects.create(foo='hey hey hey', bar='no no no')
        simple.save()
        self.assertTrue(models.SimpleObject.objects.filter(id=simple.id))
