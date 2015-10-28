from django.apps import apps
from django.db import models

import six

from .swap import get_class_object


def validate_or_get_model(cls):
    """
    Returns the class iff the reference to the model is string/unicode
    """
    if isinstance(cls, six.string_types) or isinstance(cls, six.text_type):
        try:
            return apps.get_model(cls)
        except:
            return get_class_object(cls)
    else:
        return cls


def get_cls_ptr(cls):
    """
    Returns the name of the class pointer for a given OneToOne relationship.
    """
    cls = validate_or_get_model(cls)
    return '{}_ptr'.format(cls._meta.object_name.lower())


def get_app_reference(cls):
    """
    Return simplified App Model reference e.g., app_label.ModelName
    """
    return '{0}.{1}'.format(cls._meta.app_label, cls._meta.object_name)


def get_one_to_one_field_config(cls):
    """
    Returns the models.OneToOneField necessary for the migration file.
    Parent Class specific currently.
    """
    cls = validate_or_get_model(cls)
    app_reference = get_app_reference(cls)
    return models.OneToOneField(
        parent_link=True, auto_created=True, primary_key=True, serialize=False, to=app_reference
    )


def get_swap_field(cls):
    """
    Returns the appropriately configured field for a swapped model in a migration
    """
    cls = validate_or_get_model(cls)
    ptr = get_cls_ptr(cls)
    rel = get_one_to_one_field_config(cls)
    return (ptr, rel)
