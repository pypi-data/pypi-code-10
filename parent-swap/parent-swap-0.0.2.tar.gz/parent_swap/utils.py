from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, connections, models
from django.db.migrations.loader import MigrationLoader

import six

from .swap import get_class_object


def validate_or_get_model(cls):
    """
    Returns the class if the reference to the model is string/unicode
    """
    if isinstance(cls, six.string_types) or isinstance(cls, six.text_type):
        try:
            return apps.get_model(cls)
        except:
            return get_class_object(cls)
    else:
        return cls


def is_base_model(cls):
    """
    Returns Boolean response evaluating if the provided class is django.db.models.Model
    """
    return bool(cls == models.Model)
