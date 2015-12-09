from __future__ import unicode_literals

from django.db.models import Count

from .models import Ticket, Queue, TicketCustomfieldValue


def get_statuses():
    return Ticket.objects.values_list('status', flat=True).distinct()


def get_queues():
    return Queue.objects.all()


def get_stats_for_queue(queues=None):
    all_queues = get_queues().values_list('name', flat=True)
    qs = Ticket.objects
    if queues:
        # Prevent JOIN relation and assure names exist
        queues = [str(queue) for queue in queues if str(queue) in all_queues]
        qs = qs.filter(queue__name__in=queues)
    result = qs.values('queue__name', 'status').annotate(count=Count('status')).order_by()
    stats = {}
    for stat in result:
        queue = stat['queue__name']
        status = stat['status']
        count = stat['count']
        contents = stats.get(queue, {})
        contents[status] = count
        stats[queue] = contents
    return stats


def get_stats_for_customfield(customfields=None):
    qs = TicketCustomfieldValue.objects
    if customfields:
        qs = qs.filter(customfield__name__in=customfields)
    result = qs.values('customfield__name', 'content').annotate(count=Count('ticket__status'))
    stats = {}
    for stat in result:
        customfield = stat['customfield__name']
        content = stat['content']
        count = stat['count']
        contents = stats.get(queue, {})
        contents[status] = count
        stats[queue] = contents
    return stats
