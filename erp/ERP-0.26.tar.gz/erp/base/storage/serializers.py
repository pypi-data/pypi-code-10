__author__ = 'cltanuki'
from rest_framework import serializers

from . import models
from erp.base.directory.serializers import PersonNameSerializer

# CategorySerializer.base_fields['child_cat'] = CategorySerializer(many=True)
# #


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('title', 'slug', 'pic', 'child_cat')


class CategoryStringSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('title', 'slug')


class NomenclatureSerializer(serializers.ModelSerializer):
    cat = CategoryStringSerializer()

    class Meta:
        model = models.Nomenclature
        fields = ('title', 'slug', 'cat', 'adopted')


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('title', 'slug', 'pic', 'parent', 'nomenclatures')


class DynamicItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DynamicItem
        fields = ('id', 'title', 'slug', 'desc', 'quantity', 'adopted')


class StaticItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StaticItem
        fields = ('id', 'title', 'slug', 'desc', 'invent_no', 'pos')
