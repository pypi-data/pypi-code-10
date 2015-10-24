import datetime, re, os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from subprocess import Popen, PIPE

'''
Compare version strings
Returns '0' if version1 == verstion2
Returns '-1' if version1 < version2
Returns '1' if version1 > version2
'''
def cmpv(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

'''
Return number as string with commas
'''
def commas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

'''
Format bytes into human readable numbers
'''
def bytesfmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                    return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

'''
Sends email using sendmail
'''
def sendmail(send_from, send_to, subject, body, files=None, server="127.0.0.1"):
    assert isinstance(send_to, list)
    if files:
        assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % os.path.basename(f),
                Name=os.path.basename(f)
            ))
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, stdout=PIPE, stderr=PIPE,)
    out, err = p.communicate(msg.as_string())
    return out, err

'''
Return timestamp string for logs
'''
def timestamp(fmt='%c'):
    import datetime
    return datetime.datetime.now().strftime(fmt)
