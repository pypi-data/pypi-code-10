# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import mail_admins
from yamoney.forms import YandexNotificationForm
from yamoney import settings


class NotificationView(CreateView):
    form_class = YandexNotificationForm
    http_method_names = ('post',)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        if settings.MAIL_ADMINS_ON_TRANSACTION_ERROR:
            mail_admins(
                'Yamoney error',
                'form data: {form_data}\n\nform errors: {form_errors}'.format({
                    'form_data': self.request.POST,
                    'form_errors': form.errors.as_text()
                }),
            )
        return HttpResponseBadRequest()

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse()