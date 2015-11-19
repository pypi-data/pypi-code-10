from coreinit.utils.installer import *
from coreinit.utils.template import render
from coreinit.logger import Logger
import subprocess
import os


class AutoDiscoverMixin(object):
    def _autodiscover_configure(self):
        Logger.info('Configure Avahi autodiscover driver')
        install_system(['avahi-daemon', 'avahi-discover', 'avahi-utils'])


    def _autodiscover_add_service(self, service_name, port):
        Logger.info('Add Avahi service %s' % service_name)
        template = render('avahi.conf', {'name': service_name, 'port': port, 'host': ''})
        f = open('/etc/avahi/services/%s.service' % service_name, 'w')
        f.write(template)
        f.close()

        subprocess.call(['service', 'avahi-daemon', 'restart'])


    def _autodiscover_remove_service(self, service_name):
        Logger.info('Remove Avahi service %s' % service_name)
        os.remove('/etc/avahi/services/%s.service' % service_name)

        subprocess.call(['service', 'avahi-daemon', 'restart'])


    def _get_services(self, name):
        '''
        Get CoreInit service by name
        '''
        Logger.info('Looking for Avahi services %s' % name)

        p = subprocess.Popen(['avahi-browse',
                             '-t',
                             '-p',
                             '-r',
                             '_coreinit_%s._tcp' % name], stdout=subprocess.PIPE)

        p.wait()

        results = []
        for line in p.stdout.readlines():
            fields = line.split(';')
            if fields[2] == 'IPv4' and len(fields) > 7:
                results.append((fields[7], fields[8]))

        Logger.info('\tFound Avahi services: %s' % ', '.join([str(r) for r in results]))
        return results
