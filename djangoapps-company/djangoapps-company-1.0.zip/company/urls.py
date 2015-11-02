#coding:utf-8
from django.conf.urls import patterns,url
from company import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^company_list_template/$', views.company_list_template),
    url(r'^company_edit_template/$', views.company_edit_template),
    url(r'^company_change_template/$', views.company_change_template),
    url(r'^company_list/$', views.company_list),
    url(r'^company_detail/(?P<company_id>[0-9]+)/$', views.company_detail),
)
