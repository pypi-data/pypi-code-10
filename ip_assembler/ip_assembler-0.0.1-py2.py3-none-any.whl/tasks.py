# coding=utf-8
import logging
import imaplib
import os
import re

from . import app_settings

from .models import (
    IP,
    LocationLocal
)

from celery.task import (
    PeriodicTask,
    Task,
)

from datetime import timedelta

from django.conf import settings

from shared.utils import list_remove_duplicates


logger = logging.getLogger('ip_assembler')


class UpdateLocationsIfNecessaryTask(PeriodicTask):
    """
    Tasks that checks if at least settings.IP_ASSEMBLER_IP_CHANGED_THRESHOLD IPs have changed since last run.
    If so, it calls the UpdateHtaccessLocationsTask.
    Last changed dates is written in settings.IP_ASSEMBLER_IP_CHANGED_FILE.
    """
    run_every = timedelta(minutes=60)

    def run(self, **kwargs):
        """
        Does the magic!
        """
        logger.info('UpdateLocationsIfNecessaryTask was called')

        # read last ip count
        try:
            with open(app_settings.IP_ASSEMBLER_IP_CHANGED_FILE, 'r') as f:
                content_list = f.readlines()
                if len(content_list) == 0:
                    ip_count_old = -1
                else:
                    ip_count_old = int(content_list[0])
        except IOError:
            ip_count_old = -1

        logger.info('read IP count of %(count)d' % {'count': ip_count_old})

        # if IPs have significantly changed, update the locations
        ip_count_now = IP.objects.count()
        if ip_count_now == -1 or ip_count_now > ip_count_old + app_settings.IP_ASSEMBLER_IP_CHANGED_THRESHOLD:
            logger.info('Checking IP counts, last: %(ip_count_old)d - now: %(ip_count_now)d' % {
                'ip_count_old': ip_count_old,
                'ip_count_now': ip_count_now
            })

            # call the updater task
            UpdateHtaccessLocationsTask().delay()

            # write the new count to the file
            try:
                open(app_settings.IP_ASSEMBLER_IP_CHANGED_FILE, 'w').close()
                with open(app_settings.IP_ASSEMBLER_IP_CHANGED_FILE, 'w') as f:
                    f.write(str(ip_count_now))
            except IOError:
                logger.exception('unable to write to file %(file_path)s' % {'file_path': app_settings.IP_ASSEMBLER_IP_CHANGED_FILE})
        else:
            logger.info('nothing to do here')


class UpdateHtaccessLocationsTask(Task):
    """
    Updates locations of .htaccess with new IPs.
    """
    def run(self, **kwargs):
        logger.info('UpdateHtaccessLocationsTask was called')

        # the regex patterns
        pattern0 = 'SetEnvIF REMOTE_ADDR ".*" DenyAccess'
        pattern1 = 'SetEnvIF X-FORWARDED-FOR ".*" DenyAccess'
        pattern2 = 'SetEnvIF X-CLUSTER-CLIENT-IP ".*" DenyAccess'

        for location in LocationLocal.objects.all():
            logger.info('Updating .htaccess file: %(location)s' % {'location': location.path})

            try:
                f = open(location.path, 'r')
                content_old = ''.join(f.readlines())
                f.close()
            except IOError:
                logger.exception('unable to read from file %(path)s' % {'path': location.path})
                return

            logger.info('read content of length %(length)d' % {'length': len(content_old)})

            # list of all positions of occurrences
            occurrences_r0 = [m.start(0) for m in re.finditer(pattern0, content_old)]
            occurrences_r2 = [m.start(0) for m in re.finditer(pattern2, content_old)]

            if len(occurrences_r0) == 0 or len(occurrences_r2) == 0:
                start = 0
                end = 0
            else:
                # start index where the IPs are declared
                start = occurrences_r0[0]

                # end index of IPs
                # the occurrences_r2[-1] returns only the index of the last occurrence that has a dynamic length,
                # so we search for it and append its length to get the last character
                end = occurrences_r2[-1] + len(re.findall(pattern2, content_old)[-1]) + 1

            # contents before the IPs
            content_new = content_old[:start]

            # start writing new IPs
            for ip in IP.objects.all().order_by('seg_0', 'seg_1', 'seg_2', 'seg_3'):
                replacement = '^%(seg_0)s\.%(seg_1)s\.%(seg_2)s\.%(seg_3)s$' % {
                    'seg_0': ip.seg_0,
                    'seg_1': ip.seg_1,
                    'seg_2': ip.seg_2,
                    'seg_3': ip.seg_3 if ip.seg_3 != '*' else '[0-9]+',
                }
                content_new += str(pattern0.replace('.*', replacement)) + '\n'
                content_new += str(pattern1.replace('.*', replacement)) + '\n'
                content_new += str(pattern2.replace('.*', replacement)) + '\n'

            # contents after the IPs
            content_new += content_old[end:]

            # go to beginning of file and write
            logger.info('writing new content with length %(length)d' % {'length': len(content_new)})

            # try to chmod +w the file
            try:
                os.system('chmod +w %(path)s' % {'path': location.path})
            except OSError:
                logger.exception('unable to chmod the file on path %(path)s' % {'path': location.path})

            # write to the file
            try:
                f = open(location.path, 'w')
                f.write(content_new)
                f.close()
            except IOError:
                logger.exception('unable to write to file %(path)s' % {'path': location.path})
                return

            # remove write permissions
            try:
                os.system('chmod -w %(path)s' % {'path': location.path})
            except OSError:
                logger.exception('unable to chmod the file on path %(path)s' % {'path': location.path})

            logger.info('done')


class IPEMailChecker(PeriodicTask):
    """
    Periodic task checking the mailbox for new mails about WP spamming..
    """
    run_every = timedelta(minutes=60)

    def __init__(self):
        """
        Init method setting the regular expressions.
        """
        self.regex_expressions = [
            re.compile(".*ip_tracer/(.*)\).*", re.IGNORECASE | re.MULTILINE | re.UNICODE | re.VERBOSE),
            re.compile(".*IP address (.*) has been.*"),
            re.compile(".*Ein Host, (.*)\(.*")
        ]

    def run(self, **kwargs):
        """
        Checks the IMAP mailbox for new mails and tries to handle them.
        """
        try:
            # connect to server and login
            box = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
            box.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
            box.select()

            # search for all mails in the mailbox
            result, mail_indices = box.search(None, 'ALL')

            # if everything was ok...
            if result == 'OK':

                # check number of mails
                mail_count = len(mail_indices[0].split())
                logger.info('found %(mail_count)d mails...' % {'mail_count': mail_count})

                # iterate the mail indices and fetch the mails
                ips_created = 0
                for mail_index in mail_indices[0].split():
                    logger.info('fetching mail %(mail_index)s...' % {'mail_index': int(mail_index)})
                    # mail data is a list with a tuple
                    sub_result, mail_data = box.fetch(mail_index, '(BODY[TEXT])')
                    if sub_result == 'OK':

                        # fetch the ips
                        ips = list_remove_duplicates(
                            self.find_ips(''.join([str(data) for data in mail_data[0]]))
                        )

                        # if ips found, add them and delete the mail
                        if len(ips) > 0:
                            logger.info('found %(count)d IPs' % {'count': len(ips)})
                            ips_created += IP.batch_add_ips(ips)
                            box.store(mail_index, '+FLAGS', '\\Deleted')

                    else:
                        logger.error('fetching mail with index %(index)d failed' % {'index': mail_index})

                # finally, if ips were added, unify the IPs
                if ips_created > 0:
                    logger.info('created %(count)d IPs' % {'count': ips_created})
                    IP.unify_ips()

            else:
                logger.error('search returned not OK')

            box.close()
            box.logout()
        except:
            logger.exception('retrieving mail failed')

    def find_ips(self, text):
        """
        Uses some regex to find IPs within the text.
        :param text: the text to search in
        :type text: str
        :return: list of ips
        :rtype: list
        """
        for regex in self.regex_expressions:
            ips = regex.findall(text)
            if len(ips) > 0:
                return ips
        return []
