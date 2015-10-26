from django.shortcuts import get_object_or_404

from restify import serializers
from restify.resource.base import Resource, ResourceOptions, ResourceMeta
from restify.http.response import ApiResponse


class ModelResourceOptions(ResourceOptions):
    serializer = serializers.ModelSerializer
    model = None
    form_class = None
    queryset = None
    fields = []
    exclude = []


class ModelResourceMeta(ResourceMeta):
    options_class = ModelResourceOptions


class ModelResourceMixin(object):
    def get_queryset(self):
        if self._meta.queryset is not None:
            return self.queryset._clone()
        if self._meta.model is not None:
            return self._meta.model._default_manager.all()

        raise NotImplementedError


class ModelResource(Resource, ModelResourceMixin, metaclass=ModelResourceMeta):
    def get(self, request, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        return ApiResponse(obj)
