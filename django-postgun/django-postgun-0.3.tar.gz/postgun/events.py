import requests

from django.conf import settings

from postgun import BASE_API_URL, MailgunAPIError

DATE_FORMAT = '%a, %d %b %Y %H:%m:%S %Z'


def get_page(url, auth):
    page = requests.get(url, auth=auth)
    if page.status_code != 200:
        return {'items': []}
    return page.json()


def get_events(begin=None, end=None, ascending=True, limit=300, field=''):
    """
    Grabs all Mailgun events matching a given query, even if spread out over multiple pages.

    :param begin: datetime The time to start getting events.
    :param end: datetime The time to grab events until.
    :param ascending: Ascending or descending
    :param limit: Limit to x number of items per page
    :param field: Mailgun field filters
    :return: A list of event
    """

    MAILGUN_DOMAIN = getattr(settings, 'MAILGUN_DOMAIN')
    MAILGUN_API_KEY = getattr(settings, 'MAILGUN_API_KEY')

    api_url = BASE_API_URL % MAILGUN_DOMAIN
    auth = ("api", MAILGUN_API_KEY)

    data = {'ascending': ascending,
            'limit': limit,
            }

    if begin is not None:
        data['begin'] = begin.strftime(DATE_FORMAT)
    if end is not None:
        data['end'] = end.strftime(DATE_FORMAT)
    if field != '':
        data['field'] = field

    request = requests.get(api_url + "events", auth=auth, params=data,)

    if request.status_code != 200:
        raise MailgunAPIError(request.text)
    response = request.json()
    items = response['items']

    try:
        url = response['paging']['next']
        while True:
            page = get_page(url, auth=auth)
            if len(page['items']) == 0:
                break
            items.extend(page['items'])
            url = page['paging']['next']

    except KeyError:
        pass

    return items
