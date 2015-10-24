from django.contrib import admin
from django.contrib.auth.models import Group
from erp.extras.admin import ABCAdmin
from .models import Person, Address, Phone, Position, EMail, CorpUnit, CorpObject


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class EMailInline(admin.TabularInline):
    model = EMail
    extra = 1


class PersonAdmin(admin.ModelAdmin):

    model = Person
    inlines = (PositionInline, PhoneInline, AddressInline, EMailInline)

admin.site.unregister(Group)
admin.site.register(Person, PersonAdmin)
admin.site.register(CorpUnit, ABCAdmin)
admin.site.register(CorpObject, ABCAdmin)