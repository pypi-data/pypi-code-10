# coding: utf-8
import os
import logging

import requests
from django.conf import settings

__ALL__ = ('check_email',)

ENTRY_POINT = 'https://bpi.briteverify.com/emails.json'
TIMEOUT = 10

logger = logging.getLogger(__name__)

session = requests.session()


def check_email(email):
    """ Checks email by sending request to briteverify API
    Spec: http://docs.briteverify.com/real-time-api/
    """
    api_key = (os.environ.get('BRITEVERIFY_API_KEY', None) or
               getattr(settings, 'BRITEVERIFY_API_KEY', None))
    result = dict(valid=True, disposable=False)

    if not api_key:
        return result

    data = dict(address=email, apikey=api_key)

    try:
        response = session.get(ENTRY_POINT, data=data, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception('Briteverify service error.')
        return result

    try:
        email_info = response.json()
    except ValueError:
        logger.exception('Briteverify service error. No json received.')
        return result

    try:
        result.update(dict(
            # TODO: customize this by settings
            # http://docs.briteverify.com/status-key
            valid=email_info['status'] != 'invalid',
            disposable=email_info['disposable']
        ))
    except KeyError:
        logger.exception('Briteverify service error. Bad json data: %r',
                         email_info)

    return result
