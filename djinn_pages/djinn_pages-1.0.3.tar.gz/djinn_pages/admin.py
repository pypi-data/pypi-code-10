from django.contrib import admin
from models import MenuItem


class MenuItemAdminInline(admin.TabularInline):
    model = MenuItem


class MenuItemAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'parent', )
    list_filter = ['parent', ]
    search_fields = ['title', 'url']
    inlines = [MenuItemAdminInline]

admin.site.register(MenuItem, MenuItemAdmin)
