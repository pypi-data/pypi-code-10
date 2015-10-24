__author__ = 'vitaly'

from rest_framework import generics
from rest_framework.response import Response

from . import serializers, models


class ArticlesByCategory(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ArticleByCategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Category.objects.all()
        return queryset


class CategoriesList(generics.ListCreateAPIView):

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()




class ArticlesByTag(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ArticleByTagSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Tag.objects.all()
        #slug = self.kwargs.get('slug')
        #tag = models.Tag.objects.filter(slug=slug)
        #queryset = models.Article.objects.filter(tags__in=tag)
        return queryset


class TagsList(generics.ListCreateAPIView):

    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ArticleFullSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Article.objects.all()
        return queryset


class ArticlesList(generics.ListCreateAPIView):

    serializer_class = serializers.ArticleFullSerializer
    queryset = models.Article.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.person)



class ArticleImages(generics.ListCreateAPIView):

    serializer_class = serializers.ImageSerializer
    queryset = models.Img.objects.all()

    def get_queryset(self):
        article_slug = self.kwargs.get('slug')
        article = models.Article.objects.get(slug=article_slug)
        queryset = models.Img.objects.filter(article=article)
        return queryset

    def perform_create(self, serializer):
        article_slug = self.kwargs.get('slug')
        article = models.Article.objects.get(slug=article_slug)
        serializer.save(article=article)

class ArticleImageDetail(generics.RetrieveDestroyAPIView):

    serializer_class = serializers.ImageSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        article_slug = self.kwargs.get('slug')
        article = models.Article.objects.get(slug=article_slug)
        queryset = models.Img.objects.filter(article=article)
        return queryset