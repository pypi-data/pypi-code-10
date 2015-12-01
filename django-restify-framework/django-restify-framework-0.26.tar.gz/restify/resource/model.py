from django.db.models.fields import related
from django.shortcuts import get_object_or_404

from restify import serializers
from restify.resource.base import Resource, ResourceOptions, ResourceMeta
from restify.http.response import ApiResponse


class ModelResourceOptions(ResourceOptions):
    serializer = serializers.ModelSerializer
    model = None
    form_class = None
    queryset = None


class ModelResourceMeta(ResourceMeta):
    options_class = ModelResourceOptions


class ModelResourceMixin(object):
    def get_queryset(self):
        if self._meta.queryset is not None:
            return self._meta.queryset._clone()
        if self._meta.model is not None:
            return self._meta.model._default_manager.all()

        raise NotImplementedError


class ModelResource(Resource, ModelResourceMixin, metaclass=ModelResourceMeta):
    def _get_fields_for_model(self, model, deep=1):
        retval = []
        for field in model._meta.fields:
            f = model._meta.get_field(field.name)
            if isinstance(f, related.RelatedField) and deep < 2:
                l = self._get_fields_for_model(f.related_model, deep=deep+1)
                retval.append((field.name, l))
            else:
                retval.append(field.name)

        return retval

    @property
    def serializer(self):
        if isinstance(self._meta.serializer, type):
            field_names = self.get_fields_for_model(self.get_queryset().model)
            self._meta.serializer = self._meta.serializer(fields=field_names)

        return self._meta.serializer

    def get(self, request, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        return ApiResponse(obj)


class QuerysetResource(ModelResource):
    def get(self, request):
        objs = self.get_queryset().all()
        return ApiResponse(objs)
