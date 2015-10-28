# -*- coding: utf-8 -*-
"""
Views for subscribers. For views in Django admin see admin_views.py
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from holding_page.subscribers.forms import SubscriberForm, UnsubscribeForm
from holding_page.subscribers.models import Subscriber


def subscriber_form(request, code=None):
    """
    The default view for the app, simply provides a subscriber form
    that saves a name and email address to the subscriber database.

    If a share code is provided then it will check for a matching subscriber and record that the
    user provided that share code.

    :param request: The request object.
    :type request: HttpRequest

    :param code: A share code - this will be included if the user is accessing the
       site using a shared by an other subscriber.
    :type code: unicode
    """
    initial = {}
    if code is not None:
        get_object_or_404(Subscriber, share_code=code)
        initial['source_share_code'] = code

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subscriber:thank_you'))
    else:
        form = SubscriberForm(initial=initial)

    context = {'form': form}
    return render_to_response(
        'subscriber/subscriber_form.html',
        context,
        RequestContext(request)
    )


def unsubscribe_form(request, email=None):
    """
    View to handle unsubscriptions.

    :param request: The request object.
    :type request: HttpRequest

    :param email: The email address of the subscriber to unsubscribe.
    :type email: unicode
    """
    initial = {}
    if email is not None:
        get_object_or_404(Subscriber, email=email)
        initial['email'] = email

    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            Subscriber.objects.get(email=form.cleaned_data['email']).delete()
            return HttpResponseRedirect(reverse('subscriber:successful_unsubscribe'))
    else:
        form = UnsubscribeForm(initial=initial)

    return render_to_response(
        'subscriber/unsubscribe_form.html',
        {'form': form},
        RequestContext(request),
    )
