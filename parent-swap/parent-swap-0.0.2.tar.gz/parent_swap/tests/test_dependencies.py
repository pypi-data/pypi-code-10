from django.db import models
from django.test import override_settings

from parent_swap.dependencies import get_default_dependency, get_model_dependency
from parent_swap.tests.parent_app.models import SimpleParent

from .utils import AppReloadTestCase


@override_settings(DEFAULT_BASE_CLASS='parent_swap.tests.parent_app.models.SimpleParent')
class TestModelDependencies(AppReloadTestCase):

    def test_get_simple_parent_dependency(self):
        dependency = get_model_dependency(SimpleParent)
        self.assertEqual(dependency[0], 'parent_app')
        self.assertEqual(dependency[1], '0001_initial.py')

    def test_get_default_dependency(self):
        dependency = get_default_dependency()
        self.assertEqual(dependency[0], 'parent_app')
        self.assertEqual(dependency[1], '0001_initial.py')

    def test_get_django_model_depdency(self):
        dependency = get_model_dependency(models.Model)
        self.assertIsNone(dependency)
