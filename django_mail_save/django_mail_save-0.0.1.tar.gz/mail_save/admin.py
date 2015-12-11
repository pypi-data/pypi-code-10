from django.contrib import admin

from.models import Alternative, Email, Attachment


class AlternativesInlineAdmin(admin.StackedInline):
    model = Alternative
    extra = 0
    max_num = 0
    fields = ('body_html',)

    def get_readonly_fields(self, request, obj=None):
        fields = ['body_html',]
        if obj:
            fields += [f.name for f in self.model._meta.fields]
        return fields


class AttachmentInlineAdmin(admin.TabularInline):
    model = Attachment
    extra = 0
    max_num = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        else:
            return []


class EmailAdmin(admin.ModelAdmin):
    list_display = ('to_emails', 'subject', 'sent_at', )
    search_fields =  ('from_email', 'to_emails', 'subject', 'body',)
    inlines = [AlternativesInlineAdmin, AttachmentInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        else:
            return []


admin.site.register(Email, EmailAdmin)
