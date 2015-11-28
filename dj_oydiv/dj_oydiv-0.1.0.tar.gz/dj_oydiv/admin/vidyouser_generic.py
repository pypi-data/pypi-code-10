from __future__ import absolute_import, unicode_literals

import logging

from django.core.exceptions import ValidationError, PermissionDenied
from django import forms
from django.db import router
from django.contrib import messages
from django.contrib.admin.actions import delete_selected
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.contrib import admin
try:
    # django >= 1.8
    from django.contrib.admin.utils import get_deleted_objects
except ImportError:
    from django.contrib.admin.util import get_deleted_objects

from ..models import VidyoUserBase, VidyoAdmin
from ..utils.random import random_string

logger = logging.getLogger(__name__)


class _VidyoUserModelFormTemplate(forms.ModelForm):
    search_fields = ('client_id', 'name', 'displayName')
    user_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        help_text=_("Enter password to confirm")
    )

    def clean(self, *args, **kwargs):
        """
        Make sure that the user is providing their password
        so we can encrypt/decrypt the model appropriately.
        """
        data = super(_VidyoUserModelFormTemplate, self).clean(*args, **kwargs)
        user_password = data.get('user_password')

        user = data.get('dj_auth_user', None) or self.current_user
        data['dj_auth_user'] = user
        #TODO add user permissions checking.
        #If user can create  models then they can assign to the
        #VidyoAdmin of their choice.
        #If the user can't create VidyoAdmin  objects, then
        if user_password:
            if not user.check_password(user_password):
                raise ValidationError(
                    {'user_password': [_("Admin Password is incorrect")]}
                )
        else:
            raise ValidationError(
                _("Password required")
            )
        return self.cleaned_data


class _VidyoUserModelAdminTemplate(admin.ModelAdmin):
    actions = ['delete_selected_vidyo_models']
    search_fields = ('portal_displayname', 'extension', 'client_id')
    list_display = (
        'portal_displayname', 'portal_extension', 'portal_name', 'client_id',
        'can_call', 'can_host', 'can_record', 'vidyo_entity_id'
    )

    def __init__(self, *args, **kwargs):
        """__init__ is overidden so that self is accessible to retrieve appname
        This is to avoid having to hardcode this in case it resides in a
        different namespace per project.
        """
        super(_VidyoUserModelAdminTemplate, self).__init__(*args, **kwargs)
        app_label = VidyoAdmin()._meta.app_label

        confirm = '%s/delete_selected_confirmation.html' % app_label
        delete = '%s/delete_confirmation.html' % app_label
        self.delete_selected_confirmation_template = confirm
        self.delete_confirmation_template = delete

    def get_actions(self, request):
        """we need to remove the deletion option to use our own instead of the default_proxy
        because the default does not require passwords"""
        actions = super(_VidyoUserModelAdminTemplate, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_selected_vidyo_models(self, request, queryset):
        """The first half of this method is copied practically verbatim from
        django.contrib.admin.actions.delete_selected.  However, the actual deletion
        is done within this method because django.contrib.admin uses queryset.delete()
        for efficiency. That method precludes the use of RPC.
        """

        opts = self.model._meta

        # Check that the user has delete permission for the actual model
        if not self.has_delete_permission(request):
            raise PermissionDenied()

        using = router.db_for_write(self.model)

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, perms_needed, protected = get_deleted_objects(
            queryset, opts, request.user, self.admin_site, using
        )
        # If the POST querydict has get('post'), that means the submit button
        # has been submitted: Go ahead and delete
        if request.POST.get('post'):
            password = request.POST.get('password')
            if not password:
                self.message_user(request, _("Password Required"), messages.ERROR)
                return None
            if perms_needed:
                raise PermissionDenied()

            deleted_models = 0
            for obj in queryset:
                obj_display = force_text(obj)
                self.log_deletion(request, obj, obj_display)
                try:
                    obj.decrypt(password)
                except ValueError:
                    continue
                obj.delete()
                deleted_models += 1

            if len(queryset) > deleted_models:
                self.message_user(
                    request,
                    _("couldn't delete all %ss: some were skipped") % str(type(self)),
                    messages.WARNING
                )
            else:
                self.message_user(
                    request,
                    _("Successfully deleted %(number)s %(type)ss") %
                    {
                        'number': deleted_models,
                        'type': self.model
                    },
                    messages.SUCCESS
                )
            return None
        # If the POST doesn't contain 'post' key that means we're not yet ready
        # to do the full deletion, so let django.contrib.admin render the
        # confirmation page with our overridden template
        else:
            return delete_selected(self, request, queryset)

    def delete_model(self, request, object_id, extra_context=None):
        # if request.POST is set, the user already confirmed deletion
        if not self.has_delete_permission(request):
            raise PermissionDenied()

        password = request.POST.get('password')
        if not password:
            self.message_user(request, _("Password Required"), messages.ERROR)
            return None
        try:
            object_id.decrypt(password)
        except ValueError:
            self.message_user(request, _("Wrong Password"), messages.ERROR)
            return None
        try:
            object_id.delete()
        except Exception:
            self.message_user(
                request,
                _("An unknown error occurred during deletion"),
                messages.ERROR
            )
            return None
        self.message_user(request, _("Successfully deleted"), messages.SUCCESS)
        return None

    def get_form(self, request, obj=None, **kwargs):
        form = super(_VidyoUserModelAdminTemplate, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        if change:
            if not self.has_change_permission(request):
                logger.exception("Permissions error %s" % request)
                raise PermissionDenied()
            logger.exception("Cannot update VidyoUserBase instance")
            return self.message_user(
                request,
                _("Updating VidyoUser instances is not yet supported"),
                messages.ERROR
            )
        else:
            if not self.has_add_permission(request):
                logger.exception("Permissions error %s" % request)
                raise PermissionDenied()

        if not form.cleaned_data.get('dj_auth_user'):
            logger.debug(
                "dj_auth_user not selected in admin form:"
                "falling back to logged in user<%s>:%s", request.user, obj
            )

        password = form.cleaned_data.get('user_password')
        obj._admin_model = form.cleaned_data.get('dj_auth_user').vidyoadmin
        obj._admin_model.decrypt(password)
        if change:
            pass
            # FIXME
#            obj.change_password(password, random_string())
        else:
            obj.set_password(password, random_string())
#        obj.clean()
        obj.save()


class _VidyoUserGenericModelFormMeta(type):
    def __new__(cls, clsname, bases, attrs):
        if len(bases) != 1:
            raise ValueError(
                _("VidyoUserAdminForm requires exactly one VidyoUserBase subclass")
            )
        assert issubclass(bases[0], VidyoUserBase)

        # we cast the name with ``str()`` because Python2.x requires bytestrings for typenames
        # Python3 is happy with a unicode literal, and str() is a no-op in py3.
        class_meta = type(
            str('VidyoAdminModelFormMeta'),
            (object,),
            {'model': bases[0], 'exclude': ()}
        )
        class_dict = dict({'Meta': class_meta})

        #add user overrides (if given)
        class_dict.update(attrs)
        model_form = type(
            str(bases[0].__name__ + 'ModelForm'),
            (_VidyoUserModelFormTemplate,),
            class_dict
        )
        return model_form


class VidyoUserGenericModelAdminMeta(type):
    def __new__(cls, clsname, bases, attrs):
        if len(bases) != 1:
            raise ValueError(
                _("VidyoUserAdminForm requires exactly one base class")
            )

        class_meta = type(str('VidyoAdminModelAdminMeta'), (object,), {'model': bases[0]})
        class_dict = dict({'Meta': class_meta})
        class_dict['form'] = _VidyoUserGenericModelFormMeta(clsname, bases, attrs)
        class_dict.update(attrs)
        model_admin = type(
            str(bases[0].__name__ + 'ModelAdmin'),
            (_VidyoUserModelAdminTemplate,),
            class_dict
        )
        return model_admin


def register_all_vidyo_models(**attr_dict):
    classes = VidyoUserBase.all_vidyo_user_classes()
    model_admins = [
        VidyoUserGenericModelAdminMeta(x.__name__, (x,), attr_dict)
        for x in classes
    ]

    for klass, model_admin in zip(classes, model_admins):
        logger.debug("registering %r:%r with the django admin", klass, model_admin)
        admin.site.register(klass, model_admin)
