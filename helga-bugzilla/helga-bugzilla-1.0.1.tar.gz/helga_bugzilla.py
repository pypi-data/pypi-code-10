import bugzilla
import re
from helga.plugins import match
from helga import log, settings

logger = log.getLogger(__name__)

regex = re.compile(
    r'(.*)(bugzilla|bug|bz|rhbz)\s+(#[0-9]+|[0-9]+)', re.IGNORECASE
)

def is_ticket(message):
   return regex.match(message)


def sanitize(match):
    """
    this function sanitizes the match from a ``regex.match(phrase)``
    call to return the ticket id only.
    """
    if not match:
        return ''
    ticket_id = match[-1]  # Always the last one in the group
    ticket_id = ticket_id.strip()  # probably not necessary?
    return ticket_id.strip('#')


def get_bug_subject(bug, ticket_number):
    try:
       return bug.summary
    except Exception as err:
        logger.warning("Problem looking up subject for BZ %s: %s" % (ticket_number, err))
        # If we can't look up the subject, return a default string.
        return 'unable to read subject'


def get_bug_url(settings, bug, ticket_number):
    try:
        return settings.BUGZILLA_TICKET_URL % {'ticket': ticket_number}
    except AttributeError:
        logger.debug("BUGZILLA_TICKET_URL is undefined; using API's weburl")
    try:
        return bug.weburl
    except Exception as err:
        logger.warning("Problem looking up URL for BZ %s: %s" % (ticket_number, err))
        # If we can't look up the subject, return a default string.
        return None


@match(is_ticket, priority=0)
def helga_bugzilla(client, channel, nick, message, matches):
    """
    Match possible Bugzilla tickets, return links and subject info
    """
    ticket_number = sanitize(matches.groups())

    if not ticket_number:
        logger.warning('I could not determine the right ticket from matches: %s' % matches.groups())
        # If we can't figure out the ticket number, just bail.
        return

    if not settings.BUGZILLA_XMLRPC_URL:
        logger.warning("Add BUGZILLA_XMLRPC_URL to your settings.py file.")
        return

    try:
        bz = bugzilla.Bugzilla(url=settings.BUGZILLA_XMLRPC_URL)
        bug = bz.getbugsimple(ticket_number)
    except Exception as err:
        logger.warning("Problem with Bugzilla API with url=%s: %s" % (settings.BUGZILLA_XMLRPC_URL, err))
        # If we had Bugzilla API problems, just bail.
        return

    ticket_url = get_bug_url(settings, bug, ticket_number)

    if not ticket_url:
        # If we can't find a URL, just bail.
        return

    ticket_subject = get_bug_subject(bug, ticket_number)

    return "%s might be talking about %s [%s]" % (nick, ticket_url, ticket_subject)
