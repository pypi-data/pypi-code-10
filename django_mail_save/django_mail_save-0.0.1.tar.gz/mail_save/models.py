#-*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe


class Email(models.Model):
    from_email = models.CharField(blank=True, default='', max_length=255)
    to_emails = models.TextField(blank=True, default='')
    cc_emails = models.TextField(blank=True, default='')
    bcc_emails = models.TextField(blank=True, default='')
    all_recipients = models.TextField(blank=True, default='')
    headers =  models.TextField(blank=True, default='')
    subject = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')
    raw = models.TextField(blank=True, default='')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-sent_at',)

    def __unicode__(self):
        return u'Email sent from "%s" to "%s" about "%s"' % (
            self.from_email, self.to_emails, self.subject)

    def __str__(self):
        return self.__unicode__()


class Alternative(models.Model):
    email = models.ForeignKey(Email, related_name='alternatives')
    type = models.CharField(blank=True, default='', max_length=255)
    body = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('type',)

    def __unicode__(self):
        return self.type

    def __str__(self):
        return self.__unicode__()

    def body_html(self):
        return mark_safe(self.body)


def email_attachment_path(instance, filename):
    return 'mail_save/{0}/{1}'.format(instance.email.id, filename)


class Attachment(models.Model):
    email = models.ForeignKey(Email, related_name='attachments')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=email_attachment_path)
    mimetype = models.CharField(max_length=255, null=True, blank=True,
                                default=None)

    class Meta:
        ordering = ('file_name',)

    def __unicode__(self):
        return self.file_name

    def __str__(self):
        return self.__unicode__()
