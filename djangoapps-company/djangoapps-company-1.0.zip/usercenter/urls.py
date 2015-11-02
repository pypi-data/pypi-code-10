__author__ = 'xueqing'
from django.conf.urls import patterns,url
from usercenter import views

urlpatterns = patterns(
    '',
    url(r'^login', views.login_html, name='login_html'),
    url(r'^register', views.register_html, name='register'),
    url(r'^changepwd', views.changepwd_html, name='changepwd'),
    url(r'logout',views.logout_user,name='logout'),
    url(r'^index', views.index, name='index'),
)