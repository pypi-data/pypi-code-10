#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.utils import prepare_send_to_field, smtp_send_email


def main():
    inbox = "inbox"
    password = "password"
    port = 2525
    to = [("Rcpt1", "rcpt1@example.com"), ("Rcpt2", "rcpt2@example.com"), ("", "rcpt3@example.com")]
    emails = [t[1] for t in to]
    to = prepare_send_to_field(to)
    n = 3
    body_fmt = u"you you привет {}"
    subject_fmt = u"Test subject хэллоу {}"
    file_content = "file content"
    for i in range(n):
        smtp_send_email(
            to, subject_fmt.format(i), u"Me <asdf@exmapl.com>", body_fmt.format(i),
            user=inbox, password=password, port=port, emails=emails,
            attachments=[(u"tасдest.txt", file_content)]
        )


main()
