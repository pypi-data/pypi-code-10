from __future__ import absolute_import, unicode_literals

from django.contrib.admin import site

from .override_password_form import monkeypatch_password_form
from .vidyoadmin import VidyoAdmin, VidyoAdminAdmin
from .vidyouser_generic import register_all_vidyo_models


monkeypatch_password_form()
register_all_vidyo_models()
site.register(VidyoAdmin, VidyoAdminAdmin)
