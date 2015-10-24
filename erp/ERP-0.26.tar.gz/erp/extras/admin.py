__author__ = 'cltanuki'
from django.contrib import admin


class ABCAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
