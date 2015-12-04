from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

if 'django_mptt_admin' in settings.INSTALLED_APPS:  # pragma: no cover
    from django_mptt_admin.admin import DjangoMpttAdmin as MPTTModelAdmin
else:
    from mptt.admin import MPTTModelAdmin

from .models import Item


class ItemAdmin(MPTTModelAdmin):
    """
    Admin class for the ItemAdmin class.
    """
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('href', )
    fieldsets = (
        (_('Basic settings'), {
            'fields': ('parent', 'name', 'slug', )
        }),
        ('URL', {
            'fields': ('url', ('content_type', 'object_id'), 'href'),
            'description': _("The URL for this navigation item, it can be "
                             "an absolute or relative URL, a django url pattern "
                             "or a generic relation to a model that supports get_absolute_url()"
                             "The url field has priority upon the generic relation."
                             "The link field displays the generated url.")
        }),
        (_('Access settings'), {
            'classes': ('collapse',),
            'fields': ('access_loggedin', 'access_group', 'access_permissions')
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': ('css_class', 'is_new_tab')
        })
    )
    level_limit = None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Overrides parent class formfield_for_foreignkey method."""
        # If level_limit is set filter levels depending on the limit.
        if db_field.name == "parent" and self.level_limit is not None:
            kwargs["queryset"] = self.model.objects.filter(level__lt=self.level_limit)
        return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Item, ItemAdmin)
