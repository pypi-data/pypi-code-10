from django.contrib import admin

from . import models


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }


# Register your models here.
admin.site.register(models.Tag, ArticleAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category)
admin.site.register(models.Img)