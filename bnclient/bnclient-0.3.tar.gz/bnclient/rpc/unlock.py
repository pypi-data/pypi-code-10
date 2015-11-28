# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class unlock (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'target':['-t', '--target', 'TARGET', 'Target datastore'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    # input missing operation parameters
    def fill(self, params={}):
        if params.has_key('target') == False or params['target'] == '':
            params.update({'target':raw_input('Enter Target datastore: ')})

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <unlock>\n\
    <target><%s/></target>\n\
  </unlock>\n\
</rpc>\n" % (params['messageid'], params['target'])

        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<ok' not in params['recvmsg']:
            print 'RPC <unlock> failed:'
            print params['recvmsg']
        params.update({'writemsg':''})

    def writemsg(self, params={'writemsg':''}):
        pass


