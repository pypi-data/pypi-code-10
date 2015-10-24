__author__ = 'cltanuki'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from erp.extras.admin import ABCAdmin
from .models import CorpUser, Corporation
from .forms import AdminUserChangeForm, UserCreationForm


# class PositionInline(admin.TabularInline):
#     model = Position
#     extra = 1


class CorpUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = AdminUserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', )
    list_filter = ('groups', )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name', 'mid_name')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', )
    # ordering = ('first_name', 'last_name')
    filter_horizontal = ()

    # prepopulated_fields = {"slug": ("username",)}

    # inlines = (PositionInline, )



admin.site.register(Corporation)
admin.site.register(CorpUser, CorpUserAdmin)