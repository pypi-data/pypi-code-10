# -*- coding: utf-8 -*-

import json

from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import Message
from .forms import MessageCreateForm


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'writeback/button.html'
    success_url = '.'

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(MessageCreateView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.save()
        context = {'form': form}
        message = render_to_string('writeback/email_notification.html', context)
        msg = EmailMultiAlternatives(settings.WRITEBACK_EMAIL_NOTIFICATION_SUBJECT, message,
                                     settings.WRITEBACK_EMAIL_NOTIFICATION_FROM,
                                     settings.WRITEBACK_EMAIL_NOTIFICATION_TO_LIST)
        msg.content_subtype = "html"
        msg.send()
        if self.request.is_ajax():
            return HttpResponse()
        else:
            return HttpResponseRedirect(self.get_success_url())
