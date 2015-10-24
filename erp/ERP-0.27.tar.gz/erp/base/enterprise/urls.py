__author__ = 'cltanuki'
from django.conf.urls import patterns, url, include
from django.views.generic import DetailView, DeleteView, CreateView
from rest_framework import routers

from . import views, api
from erp.base.directory import models

router = routers.SimpleRouter()
router.register(r'users', api.UserViewSet)

urlpatterns = patterns('',
    # url(r'^login/$', views.Login.as_view(), name='login'),
    # url(r'^login/ajax/$', views.AjaxLogin.as_view(), name='ajax-login'),
    url(r'^login/$', api.LoginView.as_view(), name='login'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^$', views.StructureMain.as_view(), name='structure'),
    url(r'^index/$', views.Index.as_view(), name='structure-index'),
    url(r'^user/(?P<slug>.+)/$', views.Profile.as_view(), name='user-detail'),
    url(r'^objs/$', api.ObjViewSet.as_view(), name='obj-list'),
    url(r'^units/$', api.GroupViewSet.as_view(), name='unit-list'),
    url(r'^obj/create/$', CreateView.as_view(model=models.CorpObject), name='obj-create'),
    url(r'^unit/create/$', CreateView.as_view(model=models.CorpUnit), name='unit-create'),
    url(r'^obj/(?P<slug>.+)/$', DetailView.as_view(model=models.CorpObject), name='obj-detail'),
    url(r'^unit/(?P<slug>.+)/$', DetailView.as_view(model=models.CorpUnit), name='corpunit-detail'),
    url(r'^obj/(?P<slug>.+)/delete/$', DeleteView.as_view(model=models.CorpObject), name='obj-delete'),
    url(r'^unit/(?P<slug>.+)/delete/$', DeleteView.as_view(model=models.CorpUnit), name='unit-delete'),
    url(r'^user/(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.CorpUser,
                                                      template_name='enterprise/corpuser_detail.html'),
        name='user-detail'),
    url(r'^user/pwd/$', views.PasswordChange.as_view(), name='pwd-change'),
    url(r'^', include(router.urls)),
)