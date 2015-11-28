from __future__ import absolute_import, unicode_literals

from django.contrib.admin import ModelAdmin, TabularInline
from django.core.exceptions import ValidationError, PermissionDenied, SuspiciousOperation
from django.core.validators import URLValidator, validate_ipv46_address, RegexValidator

from django import forms
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from ..models import VidyoAdmin, IPModel


HostnameValidator = RegexValidator(URLValidator.host_re, message=_("Enter a valid hostname"))

#ASSUMPTIONS
#FIXME
# This code assumes that the VidyoAdmin object being edited is the
# same as request.user._dj_auth_user.


@python_2_unicode_compatible
class IPModelInline(TabularInline):
    """Whitelist IP address"""
    verbose_name_plural = _("Whitelisted hosts")
    verbose_name = _("IP address")
    model = IPModel
    extra = 1
    fk_name = '_admin_model'

    def clean(self, *args, **kwargs):
        self.model.clean(*args, **kwargs)

    def __str__(self):
        return _("Whitelist IP address")


class VidyoAdminForm(forms.ModelForm):
    """
    Custom form for the VidyoAdmin model with additional fields
    to allow the user to change their password.
    """
    class Meta:
        model = VidyoAdmin
        exclude = ()

    # Additional form fields which are on this form but not on the model
    current_admin_password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={'current_admin_password': 'Please enter password'},
        required=False,
        help_text=_("This is the current password of the <b>assigned owner</b>")
    )

    portal_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_portal_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    cdr_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def _clean_hostname_field(self, field_name):
        host = self.cleaned_data[field_name].strip()
        HostnameValidator(host)
        return host

    def clean_portal_host(self):
        return self._clean_hostname_field('portal_host')

    def clean_cdr_host(self):
        return self._clean_hostname_field('cdr_host')

    def clean_replay_host(self):
        return self._clean_hostname_field('replay_host')

    def clean(self, *args, **kwargs):
        """
        Make sure that if the user is changing their password that the old
        password is correct and that the 2 copies of the new one match.
        """
        errs = list()
        data = super(VidyoAdminForm, self).clean(*args, **kwargs)

        # .get() because the field isn't always on the model
        current_admin_password = data.get('current_admin_password')
        if self.instance.pk:
            try:
                self.instance.decrypt(current_admin_password)
            except ValueError:
                errs.append(
                    ValidationError(
                        _("Password is incorrect."),
                        code='current_admin_password',
                        params={'current_admin_password': ''}
                    )
                )
        else:
            if 'portal_password' not in self.changed_data or not len(data.get('portal_password')):
                errs.append(
                    ValidationError(
                        _("The portal password is required to create the model."),
                        code='portal_password',
                        params={'portal_password': ''}
                    )
                )

        # Changing assigments is not allowed after instantiation.
        # If the POST data contains this field, then someone is doing something they shouldn't
        if self.instance.pk and 'dj_auth_user' in data:
            raise SuspiciousOperation(
                _("An attempt to modify an existing ForeignKey dj_auth_user was detected")
            )
        user = data.get('dj_auth_user')
        if not user and not self.instance.pk:
            errs.append(
                ValidationError(
                    _("You must assign a user"),
                    code='dj_auth_user',
                    params={'dj_auth_user': ''})
            )

        if 'portal_password' in self.changed_data or 'confirm_portal_password' in self.changed_data:
            if current_admin_password:
                user = user or self.instance.dj_auth_user
                if not user.check_password(current_admin_password):
                    errs.append(
                        ValidationError(
                            _("Password is incorrect."),
                            code='current_admin_password',
                            params={'current_admin_password': ''}
                        )
                    )
                portal_password = data['portal_password']
                confirm_portal_password = data['confirm_portal_password']

                if portal_password != confirm_portal_password:
                    errs.append(
                        ValidationError(
                            _("Passwords do not match."),
                            code='confirm_portal_password',
                            params={'confirm_portal_password': ''}
                        )
                    )
            else:
                errs.append(ValidationError(
                    _("Password required"),
                    code='current_admin_password',
                    params={'current_admin_password': ''})
                )
        if len(errs):
            raise ValidationError(errs)
        return self.cleaned_data


class VidyoAdminAdmin(ModelAdmin):
    """
    Custom ModelAdmin class which overrides things to allow the user to
    change their password while editing a VidyoAdmin object.
    """

    form = VidyoAdminForm
    inlines = (IPModelInline,)
    list_display = ('portal_user',
                    'portal_host',
                    'replay_host',
                    'portal_prefix',
                    'ssl',
                    'use_ip_auth',
                    'user_count',
                    )
    search_fields = ['portal_user']
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'dj_auth_user',
                    'portal_host',
                    'portal_user',
                    'portal_prefix',
                    'ssl',
                    'use_ip_auth',
                    'user_proxy',
                    'user_group',
                    'user_location_tag',
                    'replay_host',
                )
            }
        ),
        (
            _("Call Detail Records options"),
            {
                'classes': ('collapse',),
                'fields': (
                    'cdr_enabled',
                    'cdr_port',
                    'cdr_host',
                    'cdr_user',
                    'cdr_password',
                )
            }
        ),
        (
            _("Portal API user password"),
            {
                'fields': (
                    'portal_password',
                    'confirm_portal_password',
                )
            }
        ),
        (_("Confirmation"), {'fields': ('current_admin_password',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.pk:
            return ['dj_auth_user']
        return list()

    def save_model(self, request, obj, form, change):
        """
        Override this method to do the password changing as well as the
        normal object saving.
        """
        if change:
            if not self.has_change_permission(request):
                raise PermissionDenied()
        if obj.pk is None:
            if not self.has_add_permission(request):
                raise PermissionDenied()

        if form.cleaned_data.get('current_admin_password'):
            current_admin_password = form.cleaned_data['current_admin_password']
            portal_password = form.cleaned_data['portal_password']
            # If current_admin_password is set and we've got to here then the
            # we just need to check whether we're interested in updating the password.
            # If not, we still have to decrypt the admin object
            if portal_password:
                if change:
                    obj.change_password(current_admin_password, portal_password)
                else:
                    obj.set_password(current_admin_password, portal_password)
            else:
                obj.decrypt(current_admin_password)
        obj.save()

        return super(VidyoAdminAdmin, self).save_model(request, obj, form, change)
