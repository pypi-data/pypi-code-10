__author__ = 'meatpuppet'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sleekxmpp
import logging
from .muc_logging.muc_logging import log

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class XmppBotBase(sleekxmpp.ClientXMPP):
    """
    xmpp bot base inspired by
    http://io.drigger.com/posts/201410252029-using-thread-based-sleekxmpp-together-with-the-asyncio-event-loop-in-python-3.html
    (and built out of the echo bot example)

    in_queue: input queue.
        if you need this, you should implement the handle_input_queue function.

    out_queue: output queue

    commands: holds a table of commands you want to define.
    the commands you define are triggered in the message handle.
        example:
            self.commands = {'help': self.send_help}

            def help(self, sender, msg):
                msg.return('that should help you')

    admins: a list of admins. used by the admins_only decorator. (see decorators.py)
    """

    def __init__(self, jid, password, commands={}, settings={}):
        if not settings:
            settings = {}
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # MUC

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message", self.muc_message)

        self.commands = commands
        self.settings = settings

        self.admins = settings.get('admins', [])


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        logging.debug('starting up!')
        self.send_presence()
        self.get_roster()
        for room_password in self.settings.get('autojoin', []):
            self.plugin['xep_0045'].joinMUC(room_password[0],
                                            self.jid.split('@')[0],
                                            # If a room password is needed, use:
                                            password=room_password[1],
                                            wait=True)

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg['body'] = msg['body'].strip()
            if msg['body'].split()[0] in list(self.commands.keys()):
                if len(msg['body']) >= 1:
                    command = msg['body'].split()[0]
                    if command in self.commands:
                        self.commands[command](self, msg)
                    else:
                        pass

    def muc_message(self, msg):
        if self.settings['muc_logging']:
            log(self, msg)

        msg['body'] = msg['body'].strip()
        if msg['body'].split()[0] in list(self.commands.keys()):
            if len(msg['body']) >= 1:
                command = msg['body'].split()[0]
                if command in self.commands:
                    self.commands[command](self, msg)
                else:
                    # msg.reply("cmd not found...").send()
                    pass



