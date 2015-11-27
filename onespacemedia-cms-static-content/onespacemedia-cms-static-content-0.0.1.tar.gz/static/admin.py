from django.contrib import admin
from .models import StaticContent


@admin.register(StaticContent)
class StaticContentAdmin(admin.ModelAdmin):
    pass
