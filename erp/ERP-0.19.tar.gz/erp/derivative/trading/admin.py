from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models
from erp.extras.admin import ABCAdmin


class ProductAssocInline(admin.ModelAdmin):
    model = models.ProductAssoc


class ProductsAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ('title', 'desc', 'cat', 'available')
    list_filter = ('cat', )

    inlines = [
        ProductAssocInline
    ]

# Register your models here.
admin.site.register(models.Product, ProductsAdmin)
admin.site.register(models.Category)
