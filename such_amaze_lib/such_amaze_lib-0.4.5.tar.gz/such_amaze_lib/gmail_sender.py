import smtplib


def send_email(user_gmail, password, to_addrs, subject, message):
    """
         Send email with a gmail address to a list of address

         :Example:

             >>> user = 'me@gmail.com'
             >>> pwd = 'password'
             >>> to = 'to@gmail.com'
             >>> obj = 'Simple test'
             >>> msg = 'Hello!'
             >>> send_email(user, pwd, to, obj, msg)
            ...

     :param user_gmail: gmail user address to log on
     :param password: gmail user address password
     :param to_addrs: list of address (or single one)
     :param subject: mail object
     :param message: mail message
     """
    to_addrs = [to_addrs] if type(to_addrs) is not list else to_addrs
    message = '\r\n'.join(['From: {}'.format(user_gmail),
                           'To: {}'.format(', '.join(to_addrs)),
                           'Subject: {}'.format(subject),
                           '',
                           message])
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(user_gmail, password)
        server.sendmail(user_gmail, to_addrs, message)
        server.close()
        print 'Email successfully sent'
    except Exception as e:
        print 'Failed to send email: {}'.format(e)
