# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from flask_mail import Message

from invenio_mail.tasks import send_email


def test_send_message_outbox(email_task_app):
    """Test sending a message using Task module."""
    with email_task_app.app_context():
        with email_task_app.extensions['mail'].record_messages() as outbox:
            msg = Message('Test1',
                          sender='test1@test1.test1',
                          recipients=['test1@test1.test1'])

            send_email(msg)

            assert len(outbox) == 1
            sent_msg = outbox[0]
            assert sent_msg.subject == 'Test1'
            assert sent_msg.sender == 'test1@test1.test1'
            assert sent_msg.recipients == ['test1@test1.test1']


def test_send_message_stream(email_task_app):
    """Test sending a message using Task module."""
    with email_task_app.app_context():
        with email_task_app.extensions['mail'].record_messages() as outbox:
            msg = Message('Test2',
                          sender='test2@test2.test2',
                          recipients=['test2@test2.test2'])

            send_email(msg)

            result_stream = email_task_app.extensions['invenio-mail'].stream
            assert result_stream.getvalue().find(
                'From: test2@test2.test2') != -1
            assert result_stream.getvalue().find('To: test2@test2.test2') != -1
            assert result_stream.getvalue().find('Subject: Test2') != -1
