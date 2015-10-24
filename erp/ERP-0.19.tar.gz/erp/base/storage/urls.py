__author__ = 'cltanuki'
from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required

from . import views, api

# router = DefaultRouter()
# router.register(r'items',        api.StorageItemViewset)
# router.register(r'nomenclature', api.NomenclatureViewset)
# router.register(r'category',     api.CategoryViewset)
# router.register(r'return',       api.AdoptionViewset)
# router.register(r'ship',         api.ShipmentViewset)

# urlpatterns = patterns('',
#     url(r'^$',                           login_required(views.Index.as_view()),            name='storage'),
#     url(r'^index/$',                     login_required(views.Index.as_view()),            name='storage-index'),
#     url(r'^nomenclature/$',              login_required(views.NomenclatureList.as_view()), name='nomenclature-list'),
#     url(r'^add-nomenclature/$',          login_required(views.AddNomenclature.as_view()),  name='add'),
#     url(r'^add-category/$',              login_required(views.AddCategory.as_view()),      name='add-category'),
#     url(r'^add-item/$',                  login_required(views.AddItem.as_view()),          name='add-item'),
#     url(r'^add-log/$',                   login_required(views.AddLog.as_view()),           name='add-log'),
#     url(r'^nomenclature/(?P<slug>.+)/$', login_required(views.NomenclatureView.as_view()), name='nomenclature-view'),
#     # url(r'^item/(?P<slug>.+)/$', DetailView.as_view(model=models.Goods, template_name='value.html'), name='storage-item'),
# )
#
# urlpatterns += router.urls
# # urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns = patterns('',
    url(r'^$', login_required(views.Index.as_view()), name='storage'),

)