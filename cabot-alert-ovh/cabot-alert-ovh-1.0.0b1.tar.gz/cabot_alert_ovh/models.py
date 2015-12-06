from os import environ as env

from django.db import models
from django.conf import settings
from django.template import Context, Template

import logging
import ovh

from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

sms_template = "Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}is back to normal{% else %}reporting {{ service.overall_status }} status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}"

logger = logging.getLogger(__name__)

class OvhSMS(AlertPlugin):
    name = "Ovh SMS"
    author = "Rachid Zarouali"

    def send_alert(self, service, users, duty_officers):

        ovhep = env.get('OVH_ENDPOINT')
        ovhak  = env.get('OVH_APPLICATION_KEY')
        ovhas = env.get('OVH_APPLICATION_SECRET')
        ovhck = env.get('OVH_CONSUMER_KEY')
        ovhsn = env.get('OVH_SERVICE_NAME')
        ovhlog = env.get('OVH_LOGIN')
        ovhsender = env.get('OVH_SENDER')

        all_users = list(users) + list(duty_officers)

        client = ovh.Client(endpoint='%s' % ovhep, application_key='%s' % ovhak, application_secret='%s' % ovhas, consumer_key='%s' % ovhck)
        mobiles = OvhUserData.objects.filter(user__user__in=all_users)
        mobiles = [m.prefixed_phone_number for m in mobiles if m.phone_number]
        c = Context({
            'service': service,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
        })
        sms_message = Template(sms_template).render(c)
        for mobile in mobiles:
            try:
                client.post('/sms/%s/users/%s/jobs' % (ovhsn, ovhlog),
                    message='%s' % sms_message,
                    receivers=['%s' % mobile],
                    sender='%s' % ovhsender,
                )
            except Exception, e:
                logger.exception('Error sending Ovh sms: %s' % e)

class OvhUserData(AlertPluginUserData):
    name = "Ovh Plugin"
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        if str(self.phone_number).startswith('+'):
            self.phone_number = self.phone_number[1:]
        return super(OvhUserData, self).save(*args, **kwargs)

    @property
    def prefixed_phone_number(self):
        return '+%s' % self.phone_number
