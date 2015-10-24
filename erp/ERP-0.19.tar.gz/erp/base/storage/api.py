__author__ = 'cltanuki'
import logging

from rest_framework import generics

from . import serializers, models

logger = logging.getLogger(__name__)


# class CategoryViewset(viewsets.ModelViewSet):
#
#     serializer_class = serializers.CategorySerializer
#     queryset = models.Category.objects.filter(parent__isnull=True)
#
#     def retrieve(self, request, *args, **kwargs):
#         self.queryset = models.Category.objects.all()
#         self.serializer_class = serializers.CategoryGoodsSerializer
#         return super(CategoryViewset, self).retrieve(request, *args, **kwargs)
#
#
# class NomenclatureViewset(viewsets.ModelViewSet):
#
#     serializer_class = serializers.NomenclatureFullSerializer
#     queryset = models.Nomenclature.objects.all()
#
#     # def retrieve(self, request, *args, **kwargs):
#     #     self.serializer_class = serializers.NomenclatureFullSerializer
#     #     return super(NomenclatureViewset, self).retrieve(request, *args, **kwargs)
#
#
# class StorageItemViewset(viewsets.ModelViewSet):
#
#     serializer_class = serializers.StorageItemSerializer
#     queryset = models.StaticItem.objects.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         self.serializer_class = serializers.StorageItemFullSerializer
#         return super(StorageItemViewset, self).retrieve(request, *args, **kwargs)
#
#
# class AdoptionViewset(viewsets.ModelViewSet):
#
#     serializer_class = serializers.StorageItemAdoptionLogSerializer
#     queryset = models.StorageItemAdoptionLog.objects.all()
#
#     # def perform_update(self, serializer):
#     #     item = self.get_object()  # or (the private attribute) serializer.instance
#     #     if item.item.is_available:
#     #         return 'Итем нечестно изъяли со склада!!!'
#     #     else:
#     #         serializer.save()
#
#
# class ShipmentViewset(viewsets.ModelViewSet):
#
#     serializer_class = serializers.StorageItemShipmentLogSerializer
#     queryset = models.StorageItemShipmentLog.objects.all()
#
#     # def perform_update(self, serializer):
#     #     item = self.get_object()  # or (the private attribute) serializer.instance
#     #     if not item.item.is_available:
#     #         return 'Забыли принять!'
#     #     else:
#     #         serializer.save()
#
# # class CategoryGoodsViewset(mixins.ListModelMixin,
# #                       generics.GenericAPIView):
# #
# #     serializer_class = serializers.CategoryGoodsSerializer
# #
# #     def get(self, request, *args, **kwargs):
# #         cat_slug = self.kwargs.get('cat')
# #         logger.error(cat_slug)
# #         cat = models.Category.objects.get(slug=cat_slug)
# #         self.queryset = models.Goods.objects.filter(cat=cat)
# #         return self.list(request, *args, **kwargs)


class CategoriesList(generics.ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.filter(parent_id=None)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 100


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = models.Category
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return models.Category.objects.filter(slug=self.kwargs['slug'])


class NomenclaturesList(generics.ListCreateAPIView):
    serializer_class = serializers.NomenclatureSerializer
