# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseBadRequest
from yamoney.forms import YandexNotificationForm


class NotificationView(CreateView):
    form_class = YandexNotificationForm
    http_method_names = ('post',)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse()