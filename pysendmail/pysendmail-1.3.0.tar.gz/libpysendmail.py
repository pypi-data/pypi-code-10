# pysendmail
# author, maintainer: Ondrej Sika, <ondrej@ondrejsika.com>
# license: MIT <https://ondrejsika.com/license/mit.txt>


import smtplib


def sendmail(email_from, email_to, message, username, password, server, tls):
    server = smtplib.SMTP(server)
    if tls:
        server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, message)
    server.quit()

