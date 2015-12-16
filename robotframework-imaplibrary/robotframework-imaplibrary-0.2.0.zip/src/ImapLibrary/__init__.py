#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2015 Richard Huang <rickypc@users.noreply.github.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
IMAP Library - a IMAP email testing library.
"""

from ImapLibrary.version import get_version
from re import findall
import imaplib
import time
import urllib2
import email

__version__ = get_version()


class ImapLibrary(object):
    # pylint: disable=line-too-long
    """ImapLibrary is an email testing library for [http://goo.gl/lES6WM|Robot Framework].

    *Non-Backward Compatible Warning*

    There are inevitable changes to parameter names that would not be backward compatible with
    release 0.1.4 downwards.
    These changes are made to comply with Python code style guide on
    [https://goo.gl/NxxD0n|Method Names and Instance Variables].

    Example:
    | `Open Mailbox`   | server=imap.googlemail.com | user=email@gmail.com                | password=secret |
    | ${LATEST} =      | `Wait For Mail`            | from_email=noreply@domain.com       | timeout=300     |
    | ${HTML} =        | `Open Link From Mail`      | ${LATEST}                           |                 |
    | `Should Contain` | ${HTML}                    | Your email address has been updated |                 |
    | `Close Mailbox`  |                            |                                     |                 |

    Multipart Email Example:
    | `Open Mailbox`   | server=imap.googlemail.com | user=email@gmail.com                | password=secret |
    | ${LATEST} =      | `Wait For Mail`            | from_email=noreply@domain.com       | timeout=300     |
    | ${parts} =       | `Walk Multipart Email`     | ${LATEST}                           |                 |
    | :FOR             | ${i}                       | IN RANGE                            | ${parts}        |
    | \\               | `Walk Multipart Email`     | ${LATEST}                           |                 |
    | \\               | ${content-type} =          | `Get Multipart Content Type`        |                 |
    | \\               | `Continue For Loop If`     | '${content-type}' != 'text/html'    |                 |
    | \\               | ${payload} =               | `Get Multipart Payload`             | decode=True     |
    | \\               | `Should Contain`           | ${payload}                          | your email      |
    | \\               | ${HTML} =                  | `Open Link From Mail`               | ${LATEST}       |
    | \\               | `Should Contain`           | ${HTML}                             | Your email      |
    | `Close Mailbox`  |                            |                                     |                 |
    """
    # pylint: disable=line-too-long

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """ImapLibrary can be imported without argument.

        Examples:
        | = Keyword Definition =  | = Description =       |
        | Library `|` ImapLibrary | Initiate Imap library |
        """
        self._email_index = None
        self._imap = None
        self._mails = []
        self._mp_iter = None
        self._mp_msg = None
        self._part = None
        self._port = 993

    def open_mailbox(self, server, user, password):
        """Open the mailbox on a mail server with a valid authentication.
        """
        self._imap = imaplib.IMAP4_SSL(server, self._port)
        self._imap.login(user, password)
        self._imap.select()
        self._init_multipart_walk()

    def wait_for_mail(self, from_email=None, to_email=None, status=None, timeout=60):
        """
        Wait for an incoming mail from a specific sender to
        a specific mail receiver. Check the mailbox every 10
        seconds for incoming mails until the timeout is exceeded.
        Returns the mail number of the latest email received.

        ``status`` is a mailbox status filter.
        Please see [https://goo.gl/3KKHoY|Mailbox Status] for more information.

        `timeout` sets the maximum waiting time until an error is raised.
        """
        end_time = time.time() + int(timeout)
        while time.time() < end_time:
            self._mails = self._check_emails(from_email, to_email, status)
            if len(self._mails) > 0:
                return self._mails[-1]
            if time.time() < end_time:
                time.sleep(10)
        raise AssertionError("No mail received within time")

    def get_links_from_email(self, email_index):
        '''
        Finds all links in an email body and returns them

        `email_index` is the index number of the mail to open
        '''
        body = self.get_email_body(email_index)
        return findall(r'href=[\'"]?([^\'" >]+)', body)

    def get_matches_from_email(self, email_index, regexp):
        """
        Finds all occurrences of a regular expression
        """
        body = self.get_email_body(email_index)
        return findall(regexp, body)

    def open_link_from_mail(self, email_index, link_index=0):
        """
        Find a link in an email body and open the link.
        Returns the link's html.

        `email_index` is the index number of the mail to open
        `link_index` declares which link shall be opened (link
        index in body text)
        """
        urls = self.get_links_from_email(email_index)

        if len(urls) > link_index:
            resp = urllib2.urlopen(urls[link_index])
            content_type = resp.headers.getheader('content-type')
            if content_type:
                enc = content_type.split('charset=')[-1]
                return unicode(resp.read(), enc)
            else:
                return resp.read()
        else:
            raise AssertionError("Link number %i not found!" % link_index)

    def delete_email(self, email_index):
        """
        Delete the selected email.
        """
        self._imap.store(email_index, '+FLAGS', '\\Deleted')
        self._imap.expunge()

    def close_mailbox(self):
        """
        Close the mailbox after finishing all mail activities of a user.
        """
        self._imap.close()

    def mark_as_read(self):
        """
        Mark all received mails as read
        """
        for mail in self._mails:
            self._imap.store(mail, '+FLAGS', r'\SEEN')

    def get_email_body(self, email_index):
        """
        Returns an email body

        `email_index` is the index number of the mail to open
        """
        if self._is_walking_multipart(email_index):
            body = self.get_multipart_payload(decode=True)
        else:
            body = self._imap.fetch(email_index, '(BODY[TEXT])')[1][0][1].decode('quoted-printable')
        return body

    def walk_multipart_email(self, email_index):
        """
        Returns the number of parts of a multipart email. Content is stored internally
        to be used by other multipart keywords. Subsequent calls iterate over the
        elements, and the various Get Multipart keywords retrieve their contents.

        `email_index` is the index number of the mail to open
        """
        if not self._is_walking_multipart(email_index):
            data = self._imap.fetch(email_index, '(RFC822)')[1][0][1]
            msg = email.message_from_string(data)
            self._start_multipart_walk(email_index, msg)

        try:
            self._part = next(self._mp_iter)
        except StopIteration:
            self._init_multipart_walk()
            return False

        # return number of parts
        return len(self._mp_msg.get_payload())

    def get_multipart_content_type(self):
        """
        Return the content-type for the current part of a multipart email
        """
        return self._part.get_content_type()

    def get_multipart_payload(self, decode=False):
        """
        Return the payload for the current part of a multipart email

        decode is an optional flag that indicates whether to decoding
        """
        payload = self._part.get_payload(decode=decode)
        charset = self._part.get_content_charset()
        if charset is not None:
            return payload.decode(charset)
        return payload

    def get_multipart_field_names(self):
        """
        Return the list of header field names for the current multipart email
        """
        return list(self._mp_msg.keys())

    def get_multipart_field(self, field):
        """
        Returns the content of a header field

        field is a string such as 'From', 'To', 'Subject', 'Date', etc.
        """
        return self._mp_msg[field]

    def _check_emails(self, from_email, to_email, status):
        """Returns filtered email."""
        crit = self._criteria(from_email, to_email, status)
        # Calling select before each search is necessary with gmail
        status, data = self._imap.select()
        if status != 'OK':
            raise Exception('imap.select error: ' + status + ', ' + str(data))
        typ, msgnums = self._imap.search(None, *crit)
        if typ != 'OK':
            raise Exception('imap.search error: %s, %s, criteria=%s' % (typ, msgnums, crit))
        return msgnums[0].split()

    @staticmethod
    def _criteria(from_email, to_email, status):
        """Returns email criteria."""
        crit = []
        if from_email:
            crit += ['FROM', from_email]
        if to_email:
            crit += ['TO', to_email]
        if status:
            crit += [status]
        if not crit:
            crit = ['UNSEEN']
        return crit

    def _init_multipart_walk(self):
        """Initialize multipart email walk."""
        self._email_index = None
        self._mp_msg = None
        self._part = None

    def _is_walking_multipart(self, email_index):
        """Returns boolean value whether the multipart email walk is in-progress or not."""
        return self._mp_msg is not None and self._email_index == email_index

    def _start_multipart_walk(self, email_index, msg):
        """Start multipart email walk."""
        self._email_index = email_index
        self._mp_msg = msg
        self._mp_iter = msg.walk()
