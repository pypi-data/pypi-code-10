__author__ = 'cltanuki'
from django.conf.urls import patterns, url as url_native
from django.contrib.auth.decorators import login_required

from . import api


def url(*args, **kwargs):
    # args[1] = login_required(args[1])
    return url_native(regex=args[0], view=login_required(args[1]), **kwargs)

#
#  'url' function decorates in login_required func
#

urlpatterns = patterns('',

    #url_native(r'^api/', include(patterns('',

        url(r'^projects$', api.PrjsViewSet.as_view()),
        url(r'^tasks$', api.TasksViewSet.as_view()),

        # all items, by relationship
        # can filtered by category
        # tasks/set?type=<type>

        url(r'^projects/set$', api.PrjsSetViewSet.as_view()),
        url(r'^tasks/set$', api.TasksSetViewSet.as_view()),


        # public, owned, performing, joined
        # all on CarPrjsViewSet, CatTasksViewSet class

        url(r'^projects/public$', api.CatPrjsViewSet.as_view(), kwargs={'category':'public'}),
        url(r'^tasks/public$', api.CatTasksViewSet.as_view(), kwargs={'category':'public'}),

        url(r'^projects/owned$', api.CatPrjsViewSet.as_view(), kwargs={'category':'owned'}),
        url(r'^tasks/owned$', api.CatTasksViewSet.as_view(), kwargs={'category':'owned'}),

        url(r'^projects/performing$', api.CatPrjsViewSet.as_view(), kwargs={'category':'performing'}),
        url(r'^tasks/performing$', api.CatTasksViewSet.as_view(), kwargs={'category':'performing'}),

        url(r'^projects/joined', api.CatPrjsViewSet.as_view(), kwargs={'category':'joined'}),
        url(r'^tasks/joined', api.CatTasksViewSet.as_view(), kwargs={'category':'joined'}),

        # templates

        url(r'^projects/templates/(?P<slug>.+)/$', api.PrjTemplateDetailView.as_view()),
        url(r'^tasks/templates/(?P<slug>.+)/$', api.TaskTemplateDetailView.as_view()),

        url(r'^projects/templates$', api.PrjTemplatesViewSet.as_view()),
        url(r'^tasks/templates$', api.TaskTemplatesViewSet.as_view()),

        # project tasks

        #url(r'^projects/(?P<slug>.+)/users$', api.ProjectUsersList.as_view()),
        url(r'^projects/(?P<slug>.+)/members', api.ProjectUsersList.as_view()),

        #url(r'^tasks/(?P<slug>.+)/users$', api.TaskUsersList.as_view()),


        url(r'^projects/(?P<slug>.+)/tasks$', api.PrjTaskViewSet.as_view()),


        # details

        url(r'^projects/(?P<slug>.+)/$', api.PrjDetailView.as_view()),
        url(r'^tasks/(?P<slug>.+)/$', api.TaskDetailView.as_view()),




        #url(r'^task/assign/user$', login_required(views.TaskUserAssign.as_view())),
        # url(r'^prj/assign/user$', login_required(views.PrjUserAssign.as_view())),

)