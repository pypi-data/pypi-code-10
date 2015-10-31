from django.contrib import admin
from .models import Group, Human, OtherPeople, Extra

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'role', 'location', 'email']

@admin.register(OtherPeople)
class OtherPeopleAdmin(admin.ModelAdmin):
    pass

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ['field_name', 'value']
