from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models
from erp.extras.admin import ABCAdmin


class ShipmentLogInline(GenericTabularInline):
    model = models.StorageItemShipmentLog

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['when', 'comment']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []


class AdoptionLogInline(GenericTabularInline):
    model = models.StorageItemAdoptionLog

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['when', 'comment']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []


class StaticItemAdmin(admin.ModelAdmin):
    model = models.StaticItem
    list_display = ('pos', 'desc', 'is_available')
    list_filter = ('pos', )

    inlines = [
        ShipmentLogInline,
        AdoptionLogInline
    ]


class DynamicItemAdmin(admin.ModelAdmin):
    model = models.StaticItem
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'desc', 'quantity')
    ordering = ('quantity', )

    def get_readonly_fields(self, request, obj=None):
        return ['quantity', ]  # Return a list or tuple of readonly fields' names

    inlines = [
        ShipmentLogInline,
        AdoptionLogInline
    ]

# Register your models here.
admin.site.register(models.Category, ABCAdmin)
admin.site.register(models.StaticItem, StaticItemAdmin)
admin.site.register(models.DynamicItem, DynamicItemAdmin)
admin.site.register(models.Nomenclature, ABCAdmin)
