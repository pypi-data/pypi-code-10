# -*- coding: utf-8 -*-
"""
Holds the subscriber model which represents someone who has subscribed to updates.
"""
from uuid import uuid4
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


class Subscriber(models.Model):
    """
    A subscriber represents a visitor to the holding page who has subscribed by providing their email address.
    """
    full_name = models.CharField(_('Full name'), max_length=255)
    email = models.EmailField(_('Email address'), unique=True, db_index=True)
    share_code = models.CharField(_('Share code'), max_length=36, null=True, db_index=True)
    source_share_code = models.CharField(_('Source share code'), max_length=36, blank=True, null=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} <{1}>'.format(self.full_name, self.email)

    class Meta(object):
        permissions = (
            ('export_csv', _('Can export CSV data')),)

    @property
    def subscribers_recruited(self):
        return Subscriber.objects.filter(source_share_code=self.share_code).count()

    @staticmethod
    def share_code_generator(sender, **kwargs):
        """
        Generates a unique share code for a subscriber using a ask for
        forgiveness, not permission, system
        """
        del sender
        instance = kwargs['instance']
        if kwargs['created'] is False:
            return
        instance.share_code = uuid4()
        instance.save()

    @staticmethod
    def send_email(sender, **kwargs):
        """
        Sends a welcome email to the user informing them about the share
        code, and also information about un-subscribing
        """
        del sender
        instance = kwargs['instance']
        if kwargs['created'] is False:
            return
        site = Site.objects.get(pk=settings.SITE_ID)
        subject = render_to_string(
            'email/welcome_subject.txt',
            {'subscriber':  instance, 'site': site}
        )
        body = render_to_string(
            'email/welcome_body.txt',
            {'subscriber':  instance, 'site': site}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email]
        )


post_save.connect(Subscriber.share_code_generator, sender=Subscriber)
post_save.connect(Subscriber.send_email, sender=Subscriber)
