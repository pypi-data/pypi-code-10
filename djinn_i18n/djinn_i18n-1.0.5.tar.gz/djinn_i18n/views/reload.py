from django.contrib import messages
from djinn_core.views.admin import AdminMixin
from index import IndexView

class ReloadView(IndexView, AdminMixin):


    def get(self, request, *args, **kwargs):
        from django.utils import translation
        from django.utils.translation import trans_real
        try:
            from threading import local
        except ImportError:
            from django.utils._threading_local import local

        _thread_locals = local()

        import gettext

        try:
            # Reset gettext.GNUTranslation cache.
            gettext._translations = {}

            # Reset Django by-language translation cache.
            trans_real._translations = {}

            # Delete Django current language translation cache.
            trans_real._default = None

            messages.add_message(request, messages.SUCCESS, "Translations reloaded")

            # Delete translation cache for the current thread,
            # and re-activate the currently selected language (if any)
            prev = trans_real._active.pop(_thread_locals, None)
            if prev:
                translation.activate(prev.language())

        except AttributeError, e:
            pass

        return super(ReloadView, self).get(request, *args, **kwargs)
