from django.conf.urls import patterns, url

from .views import (
    ImportIndex, ImportNew, ImportUpload, ImportCreateCategory,
    ImportExistingCategory, ImportFailed, ImportPending, ImportReview
)

urlpatterns = patterns(
    '',
    url(
        r'^import/$',
        ImportIndex.as_view(),
        name='index'),
    url(
        r'^import/new/$',
        ImportNew.as_view(),
        name='import_new'),
    url(
        r'^import/projects/(?P<project_id>[0-9]+)/$',
        ImportUpload.as_view(),
        name='import_upload'),
    url(
        r'^import/(?P<import_id>[0-9]+)/create-category/$',
        ImportCreateCategory.as_view(),
        name='import_createcategory'),
    url(
        r'^import/(?P<import_id>[0-9]+)/existing-category/$',
        ImportExistingCategory.as_view(),
        name='import_existingcategory'),
    url(
        r'^import/(?P<import_id>[0-9]+)/error/$',
        ImportFailed.as_view(),
        name='import_error'),
    url(
        r'^import/(?P<import_id>[0-9]+)/pending-contributions/$',
        ImportPending.as_view(),
        name='import_done'),
    url(
        r'^import/(?P<import_id>[0-9]+)/pending-contributions/(?P<observation_id>[0-9]+)/$',
        ImportReview.as_view(),
        name='import_review'),
)
