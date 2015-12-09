"""django-mailer related processors."""

from mailer.models import Message

from ..constants import SERVER_STATUS

# TODO find way to make these into settings (maybe dict? only clean namespace?)
# From here up it counts as WARNING
WARNING_THRESHOLD = 1
# From here up it counts as DANGER
DANGER_THRESHOLD = 10


def deferred_emails():
    """Checks for deferred email, that otherwise fill up the queue."""
    status = SERVER_STATUS['OK']
    count = Message.objects.deferred().count()

    if WARNING_THRESHOLD <= count < DANGER_THRESHOLD:
        status = SERVER_STATUS['WARNING']
    if count >= DANGER_THRESHOLD:
        status = SERVER_STATUS['DANGER']

    return {
        'label': 'Deferred Email',
        'status': status,
        'info': 'There are currently {0} deferred messages.'.format(count)
    }
