from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin

from lab_members.models import Scientist
from lab_members.admin import ScientistAdmin

class CMSScientistAdmin(PlaceholderAdminMixin, ScientistAdmin):
    fieldsets = [
        ScientistAdmin.fieldset_basic,
        ScientistAdmin.fieldset_alumni,
        ScientistAdmin.fieldset_website,
        ScientistAdmin.fieldset_advanced,
    ]

admin.site.unregister(Scientist)
admin.site.register(Scientist, CMSScientistAdmin)
