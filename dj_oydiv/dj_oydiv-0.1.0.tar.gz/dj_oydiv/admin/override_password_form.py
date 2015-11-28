from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def monkeypatch_password_form():
    """
    Don't look at me. I'M HIDEOUS!
    On import this module monkey-patches the password change form used within
    the django admin interface, so that when a user changes her password, any
    vidyoadmin objects, and associated VidyoUserBase keys are updated.
    """
    logger.debug("Monkeypatching django admin password change form")
    oldsave = PasswordChangeForm.save

    def newsave(self, commit=True):
        logger.debug("django admin password change form: attempting to update VidyoAdmin passwords")
        # assume we don't have to do any checking whether the passwords match.
        old_key = self.cleaned_data["old_password"]
        new_key = self.cleaned_data["new_password1"]
        try:
            self.user.vidyoadmin.decrypt(old_key)
            logger.debug("successfully decrypted old VidyoAdmin object")
            self.user.vidyoadmin.change_key(old_key, new_key)
        except (ObjectDoesNotExist, AttributeError):
            # If the user does not have a vidyoadmin, we don't care
            pass
        return oldsave(self, commit)

    PasswordChangeForm.save = newsave
