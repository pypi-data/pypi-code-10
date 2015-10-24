__author__ = 'kir'

from rest_framework import generics

from . import serializers, models


class CategoriesList(generics.ListCreateAPIView):
    serializer_class = serializers.CategoriesSerializer
    queryset = models.Category.objects.all()

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 100


class ProductsList(generics.ListCreateAPIView):
    model = models.Product
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 100


class ItemsList(generics.ListCreateAPIView):
    model = models.ProductAssoc
    serializer_class = serializers.ProductAssocsSerializer

    def get_queryset(self):
        return models.ProductAssoc.objects.filter(product_id=self.kwargs['pk'])


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    model = models.Product
    serializer_class = serializers.ProductSerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = models.Category
    serializer_class = serializers.CategoriesSerializer
