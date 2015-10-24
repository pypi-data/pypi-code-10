__author__ = 'kir'
from rest_framework.serializers import ModelSerializer, RelatedField
from erp.base.storage.serializers import StaticItemSerializer, DynamicItemSerializer
from erp.base.storage.models import StaticItem, DynamicItem
from . import models


class CategoriesSerializer(ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'title', 'slug', 'parent', 'pic')


class CategoriesStringSerializer(ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('title', 'slug')


class ProductGallerySerializer(ModelSerializer):

    class Meta:
        model = models.ProductGallery
        fields = ('id', 'image')


class MaterialStringSerializer(ModelSerializer):

    class Meta:
        model = models.DynamicItem
        fields = ('title', 'slug')


class ProductAssocsSerializer(ModelSerializer):
    material = MaterialStringSerializer()

    class Meta:
        model = models.ProductAssoc
        fields = ('id', 'count', 'material')


class ProductDetailSerializer(ModelSerializer):
    items = ProductAssocsSerializer(many=True)
    gallery = ProductGallerySerializer(many=True)
    rel_cat = CategoriesStringSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ('id', 'title', 'slug', 'desc', 'logo', 'cat', 'items', 'gallery')


class ProductSerializer(ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('id', 'title', 'slug', 'logo')
