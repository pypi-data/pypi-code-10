#-*- coding: utf-8 -*-
from email.mime.base import MIMEBase

from django.core.files.base import ContentFile, File
from django.core.mail.backends.smtp import EmailBackend as base_backend
from django.utils.encoding import smart_text

from ..models import Email, Attachment


class EmailBackend(base_backend):

    def _send(self, email_message):
        sent = super(EmailBackend, self)._send(email_message)
        message_data = {
            'from_email': u'%s' % email_message.from_email,
            'to_emails': u', '.join(email_message.to),
            'cc_emails': u', '.join(email_message.cc),
            'bcc_emails': u', '.join(email_message.bcc),
            'all_recipients': u', '.join(email_message.recipients()),
            'subject': u'%s' % email_message.subject,
            'body': u'%s' % email_message.body,
            'raw': u'%s' % smart_text(email_message.message().as_string())
        }
        email = Email.objects.create(**message_data)
        if hasattr(email_message, 'alternatives'):
            for alternative in email_message.alternatives:
                body, mimetype = alternative
                email.alternatives.create(body=body, type=mimetype)
        if hasattr(email_message, 'attachments'):
            for attachment in email_message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                    django_file = ContentFile(content, filename)
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    django_file = File(attachment, filename)
                    mimetype = None
                email_attachment = Attachment(
                    email=email, file_name=filename, mimetype=mimetype)
                email_attachment.file.save(filename, django_file, save=True)
        return sent
