__author__ = 'vitaly'

from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('title', 'slug')



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Img
        fields = ('id', 'img')

class ImageFullSerializer(serializers.ModelSerializer):

    article = serializers.SlugRelatedField(
        queryset=models.Article.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = models.Img
        fields = ('id', 'article', 'img',)




class ArticleSerializer(serializers.ModelSerializer):

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=models.Tag.objects.all(),
        slug_field='slug'
    )

    cat = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = models.Article
        fields = ('title', 'slug', 'cat', 'created', 'tags')

class ArticleFullSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, read_only=True)

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=models.Tag.objects.all(),
        slug_field='slug'
    )

    cat = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = models.Article
        fields = ('title', 'slug', 'cat', 'body', 'images', 'created', 'tags')


class ArticleByTagSerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = models.Tag
        fields = ('title', 'slug', 'articles')



class CategorySerializer(serializers.ModelSerializer):

    parent = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = models.Category
        fields = ('title', 'slug', 'parent', 'pic')

class ArticleByCategorySerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(many=True, read_only=True)
    parent = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = models.Category
        fields = ('title', 'slug', 'parent', 'pic', 'articles')

