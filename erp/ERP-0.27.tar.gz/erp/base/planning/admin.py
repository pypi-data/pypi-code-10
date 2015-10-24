__author__ = 'cltanuki'
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from erp.extras.admin import ABCAdmin
from . import models


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


class TaskAdmin(ABCAdmin):
    def save_model(self, request, task, form, change):
        task.owner = request.user.person
        task.save()

class ProjectAdmin(TaskAdmin):
    pass


# Register your models here.
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(models.TaskTemplate, ABCAdmin)
admin.site.register(models.ProjectTemplate, ABCAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Project, ProjectAdmin)

admin.site.register(models.Role)