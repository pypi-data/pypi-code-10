from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import Alternative


class EmailAlternativeView(LoginRequiredMixin, DetailView):

    queryset = Alternative.objects.all()
    template_name = 'mail_save/email/alternative.html'
