# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from scaffold_toolkit.views import kindeditor_upload_file

urlpatterns = [url(r'^kind_upload/$', kindeditor_upload_file, name='kind_upload'),
               url(r'^dialog-success/$', TemplateView.as_view(template_name='common/dialog_success.html'),
                   name='dialog_success'),
               ]
