# -*- coding: utf-8 -*-
"""Views used by the characters admin."""
from __future__ import unicode_literals
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.template import loader, Context
from holding_page.subscribers.models import Subscriber


@staff_member_required
@permission_required('subscriber.export_csv')
def export_csv(request):
    """
    This admin view allows a staff member with the export_csv permission
    to produce a CSV of subscribed users
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subscriber_data.csv'
    t = loader.get_template('data/subscriber_data.csv')
    c = Context({
        'subscribers': Subscriber.objects.all(),
    })
    response.write(t.render(c))
    return response
