from . import models, serializers

__author__ = 'cltanuki'
from rest_framework import generics


class PrjParams():
    serializer_class = serializers.PrjSerializer
    model = models.Project


class TaskParams():
    serializer_class = serializers.TaskSerializer
    model = models.Task


class PrjTemplateParams():
    serializer_class = serializers.PrjTemplateSerializer
    model = models.ProjectTemplate


class TaskTemplateParams():
    serializer_class = serializers.TaskTemplateSerializer
    model = models.TaskTemplate


class ItemsViewSet(generics.ListCreateAPIView):

    def get_queryset(self):
        print(self.request.GET.get('type'))
        model = self.model
        return model.objects.all()


class PrjTaskViewSet(ItemsViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.person)


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'slug'

    def get_queryset(self):
        model = self.model
        return model.objects.all()


class CatItemsViewSet(generics.ListAPIView):
    def get_queryset(self):

        category = self.kwargs['category']
        user = self.request.user
        model = self.model

        if category == 'public':
            queryset = model.objects.filter(public=True)

        elif category == 'owned':
            queryset = model.objects.filter(owner=user)

        elif category == 'performing':
            queryset = model.objects.filter(performer=user)

        elif category == 'joined':
            if model == models.Project:
                queryset = user.person.prj_assigned_users.all()
            elif model == models.Task:
                queryset = user.person.task_assigned_users.all()

        return queryset


class ItemsSetViewSet(generics.ListAPIView):


    def get_queryset(self):

        from itertools import chain
        from operator import attrgetter
        from django.shortcuts import get_object_or_404
        from django.contrib.contenttypes.models import ContentType

        person = self.request.user.person

        if self.model == models.Task:
            owned = person.owned_tasks
            performer = person.task_performer
            joined = person.task_assigned_users

        elif self.model == models.Project:
            owned = person.owned_prjs
            performer = person.prj_performer
            joined = person.prj_assigned_users

        objects = sorted(chain(owned.all(), performer.all(), joined.all()),
                           key=attrgetter('deadline'))

        if self.request.GET.get('type') is not None:
            type_name = get_object_or_404(ContentType, name=self.request.GET.get('type'))
            objects = owned.filter(item_type=type_name)

        return objects


class PrjsViewSet(PrjParams, PrjTaskViewSet):
    pass


class TasksViewSet(TaskParams, PrjTaskViewSet):
    pass


class CatPrjsViewSet(PrjParams, CatItemsViewSet):
    pass


class CatTasksViewSet(TaskParams, CatItemsViewSet):
    pass


class PrjsSetViewSet(PrjParams, ItemsSetViewSet):

    pass


class TasksSetViewSet(TaskParams, ItemsSetViewSet):
    pass



class PrjTaskViewSet(TaskParams, ItemsViewSet):
    def get_queryset(self):
        slug = self.kwargs['slug']
        project = models.Project.objects.filter(slug=slug)
        queryset = models.Task.objects.filter(prj=project)
        return queryset



class PrjDetailView(PrjParams, ItemDetailView):
    pass


class TaskDetailView(TaskParams, ItemDetailView):
    pass






class TemplatesViewSet(ItemsViewSet):
    pass


class TemplateDetailView(ItemDetailView):
    pass


class PrjTemplatesViewSet(PrjTemplateParams, TemplatesViewSet):
    pass


class TaskTemplatesViewSet(TaskTemplateParams, TemplatesViewSet):
    pass


class PrjTemplateDetailView(PrjTemplateParams, TemplateDetailView):
    pass


class TaskTemplateDetailView(TaskTemplateParams, TemplateDetailView):
    pass


class ProjectUsersList(generics.ListCreateAPIView):

    serializer_class = serializers.PrjRoleSerializer
    queryset = models.Person.objects.all()

    def get_queryset(self):

        slug = self.kwargs.get('slug')
        project = models.Project.objects.get(slug=slug)

        role = models.PrjRole.objects.filter(prj=project)

        #users = models.Person.filter()
        return role


    def perform_create(self, serializer):
        project_slug = self.kwargs.get('slug')
        project = models.Project.objects.get(slug=project_slug)
        serializer.save(prj=project)