from django.contrib import admin
from lab_members.models import Position, Scientist, Institution, Degree, Field, Advisor, Education, Employment

class PositionAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Position, PositionAdmin)


class EducationInline(admin.TabularInline):
    model = Education
    extra = 3


class EmploymentInline(admin.TabularInline):
    model = Employment
    extra = 3


class ScientistAdmin(admin.ModelAdmin):
    fieldset_basic = ('Basic Info', {
        'fields': [
            'full_name',
            'email',
            'title',
            'photo',
            'visible',
            'current',
        ]
    })

    fieldset_alumni = ('Alumni Information', {
        'classes': ['collapse'],
        'fields': [
            'alumni_current_institution',
            'alumni_current_title',
            'alumni_redirect_url',
        ]
    })

    fieldset_website = ('Website', {
        'fields': [
            'website_url',
            'website_name',
        ],
    })

    fieldset_bio = ('Bio', {
        'fields': [
            'personal_interests',
            'research_interests',
        ],
    })

    fieldset_advanced = ('Advanced', {
        'fields': ['slug'],
        'classes': ['collapse'],
    })

    fieldsets = [
        fieldset_basic,
        fieldset_alumni,
        fieldset_website,
        fieldset_bio,
        fieldset_advanced,
    ]

    inlines = [EducationInline, EmploymentInline]

    list_display = ['full_name', 'title', 'email', 'current', 'visible']
    list_filter = ['title', 'current', 'visible']
    search_fields = ['full_name']

    prepopulated_fields = {"slug": ("full_name",)}

admin.site.register(Scientist, ScientistAdmin)


class InstitutionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Institution, InstitutionAdmin)


class RecordAdmin(admin.ModelAdmin):
    ordering = ['scientist', 'year_start', 'year_end']

    list_display = [
        'scientist_years',
        'institution',
        'field',
    ]
    list_filter = ['field']
    search_fields = [
        'scientist__full_name',
        'institution__name',
        'advisor__full_name',
    ]

    def scientist_years(self, object):
        return "{} ({})".format(object.scientist, object)

    def add_list_display(self, request, attribute):
        list_display = super().get_list_display(request)[:]
        list_display.append(attribute)
        return list_display

    def add_list_filter(self, request, attribute):
        list_filter = super().get_list_filter(request)[:]
        list_filter.append(attribute)
        return list_filter


class EducationAdmin(RecordAdmin):

    def get_list_display(self, request):
        return self.add_list_display(request, 'degree')

    def get_list_filter(self, request):
        return self.add_list_filter(request, 'degree')

admin.site.register(Education, EducationAdmin)


class EmploymentAdmin(RecordAdmin):

    def get_list_display(self, request):
        return self.add_list_display(request, 'position')

    def get_list_filter(self, request):
        return self.add_list_filter(request, 'position')

admin.site.register(Employment, EmploymentAdmin)


class DegreeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Degree, DegreeAdmin)


class FieldAdmin(admin.ModelAdmin):
    pass

admin.site.register(Field, FieldAdmin)


class AdvisorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Advisor, AdvisorAdmin)

admin.site.site_header = 'Lab Member Administration'
