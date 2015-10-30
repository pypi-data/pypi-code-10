# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class copy_config (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'target':['-t', '--target', 'TARGET', 'Target datastore'],
            'source':['-s', '--source', 'SOURCE', 'Source datastore'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    # input missing operation parameters
    def fill(self, params={}):
        if params.has_key('source') == False or params['source'] == '':
            params.update({'source':raw_input('Enter Source datastore: ')})

        if params.has_key('target') == False or params['target'] == '':
            params.update({'target':raw_input('Enter Target datastore: ')})

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <copy-config>\n\
    <target><%s/></target>\n\
    <source><%s/></source>\n\
  </copy-config>\n\
</rpc>\n" % (params['messageid'], params['target'], params['source'])

        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<ok' not in params['recvmsg']:
            print 'RPC <copy-config> failed:'
            print params['recvmsg']
        params.update({'writemsg':''})

    def writemsg(self, params={'writemsg':''}):
        pass


