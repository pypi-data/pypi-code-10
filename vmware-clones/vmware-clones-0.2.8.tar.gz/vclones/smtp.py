__author__ = 'gabriel'

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from vclones.resources import get_email_notification_template


def send_email_notifications(vms, host, datacenter, cluster, rcpt_from, rcpt_to, smtp_host):
    msg = MIMEMultipart()
    msg['Subject'] = 'Clone report on {0} [dc:{1},cl:{2}]'.format(host, datacenter, cluster)
    msg['From'] = rcpt_from
    msg['To'] = rcpt_to

    msgbody = get_email_notification_template().render(
        host=host,
        datacenter=datacenter,
        cluster=cluster,
        vms=vms,
        totalvms=len(vms)
    )
    msg.attach(MIMEText(msgbody, 'html'))

    s = smtplib.SMTP(smtp_host)
    s.sendmail(msg['From'], rcpt_to.split(', '), msg.as_string())
    s.quit()