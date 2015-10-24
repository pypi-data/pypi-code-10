__author__ = 'vitaly'

from django.conf.urls import patterns, url  # as url_native

from . import api

urlpatterns = patterns('',


        url(r'^categories/(?P<slug>.+)/$', api.ArticlesByCategory.as_view()),

        # return all categories
        url(r'^categories$', api.CategoriesList.as_view()),

        # display articles by tag (title, slug)
        url(r'^tags/(?P<slug>.+)/$', api.ArticlesByTag.as_view()),

        # return all tags
        url(r'^tags$', api.TagsList.as_view()),

        # manage one image
        url(r'^articles/(?P<slug>.+)/images/(?P<pk>.+)/$', api.ArticleImageDetail.as_view()),

        # return article images
        url(r'^articles/(?P<slug>.+)/images$', api.ArticleImages.as_view()),

        # return one article (full)
        url(r'^articles/(?P<slug>.+)/$', api.ArticleDetail.as_view()),

        # return articles list (title, slug)
        url(r'^articles$', api.ArticlesList.as_view()),

    #))),
)