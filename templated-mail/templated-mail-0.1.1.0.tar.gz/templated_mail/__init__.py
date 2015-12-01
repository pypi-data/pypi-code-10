import simple_mail as mail
import unittest.mock as mock
from .environment import MessageEnvironment
from .loader import DynamicLoader
from .template import MessageTemplate


class TemplatedMail(object):

    def __init__(self, config, logger=None):
        """
        Store config for the mail server,
        and the location of email templates.

        """

        self.config = config
        self.mail = mail.Mail(config)
        self.env = MessageEnvironment(loader=DynamicLoader(
            self.config.MESSAGE_DIR
        ))
        self.logger = logger if logger is not None else mock.Mock()

    def send_email_by_name(self, name, recipients, context=None):
        """
            1) Build the email template of `name`, as found
            under the configured message directory.
            2) Load and render the subject, text and HTML,
            as defined in <MESSAGE_DIR>/use_my_service.msg,
            with the given context.

        """

        template = self.env.get_template('{}.msg'.format(name))
        if template is not None:
            self.mail.send_message(
                recipients=recipients,
                **template.render(**context))
        else:
            self.logger.error('couldn\'t render a template.')
