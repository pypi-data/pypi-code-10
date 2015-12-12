from django.views.generic import DetailView

from .models import Alternative


class EmailAlternativeView(DetailView):

    queryset = Alternative.objects.all()
    template_name = 'mail_save/email/alternative.html'
