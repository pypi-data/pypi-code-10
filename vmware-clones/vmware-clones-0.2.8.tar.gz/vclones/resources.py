__author__ = 'gabriel'

from pkg_resources import resource_filename
from sys import prefix

#EMAIL_TEMPLATE = resource_filename(__name__, 'email_notification.html')

from jinja2 import Template


def get_email_notification_template():
    return Template(
        open('/opt/vclones/email_notification.html', 'r+').read()
    )