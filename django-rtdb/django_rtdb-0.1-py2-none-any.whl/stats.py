from __future__ import unicode_literals

from django.db.models import Count

from .models import Ticket, Queue, TicketCustomfieldValue


def get_statuses():
    return Ticket.objects.values_list('status', flat=True).distinct()


def get_queues():
    return Queue.objects.all()


def get_stats_for_queue(queue=None):
    qs = Ticket.objects
    if queue:
        qs = qs.filter(queue=queue)
    return qs.values('queue__name', 'status').annotate(count=Count('status')).order_by()


def get_stats_for_customfield(customfields=None):
    qs = TicketCustomfieldValue.objects
    if customfields:
        qs = qs.filter(customfield__name__in=customfields)
    return qs.values('customfield__name', 'content').annotate(count=Count('ticket__status'))
