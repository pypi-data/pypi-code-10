from django.db import models
from django.conf import settings
from django.views.generic.detail import DetailView

from rest_framework import serializers


__all__ = ['BaseModel', 'BaseMapping', 'BaseSerializer', 'BaseView']


def import_class(cls_path, default=None):
    try:
        mod_name, sp, cls_name = cls_path.rpartition('.')
        mod = __import__(mod_name, fromlist=[''])
        cls_obj = getattr(mod, cls_name, default)
        return cls_obj
    except:
        return default


def get_base_model():
    default_model_name = getattr(settings, 'DEFAULT_BASE_MODEL', None)
    return import_class(default_model_name, models.Model)


def get_base_mapping(base_cls):
    return getattr(base_cls, 'Mapping', object)


def get_base_serializer():
    default_serializer_name = getattr(settings, 'DEFAULT_SERIALIZER', None)
    return import_class(default_serializer_name, serializers.Serializer)


def get_base_view():
    default_view_name = getattr(settings, 'DEFAULT_VIEW', None)
    return import_class(default_view_name, DetailView)


BaseModel = get_base_model()
BaseMapping = get_base_mapping(BaseModel)
BaseSerializer = get_base_serializer()
BaseView = get_base_view()
