"""Views for the ``server_guardian`` app."""
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from . import models
from .default_settings import DASHBOARD_VIEW_PERMISSION


class GuardianDashboardView(ListView):
    model = models.Server

    @method_decorator(user_passes_test(DASHBOARD_VIEW_PERMISSION))
    def dispatch(self, request, *args, **kwargs):
        return super(GuardianDashboardView, self).dispatch(
            request, *args, **kwargs)
