__author__ = 'kir'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
# from rest_framework.routers import DefaultRouter

from . import views, api

urlpatterns = patterns('',
    url(r'^$',                          login_required(views.Index.as_view()),        name='trading-index'),
    url(r'^products/$',                 login_required(api.ProductsList.as_view()),   name='product-list'),
    url(r'^categories/$',               login_required(api.CategoriesList.as_view()), name='category-list'),
    url(r'^products/(?P<pk>.+)/$',      login_required(api.ProductDetail.as_view()),  name='product-view'),
    url(r'^products/(?P<id>.+)/sale$',  login_required(views.product_sale),           name='product-sale'),
    url(r'^products/(?P<pk>.+)/items$', login_required(api.ItemsList.as_view()),      name='product-items'),
    url(r'^categories/(?P<pk>.+)/$',    login_required(api.CategoryDetail.as_view()), name='category-view'),
)
