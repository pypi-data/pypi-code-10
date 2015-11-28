# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class kill_session (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'sessionid':['-i', '--sessid', 'SESSID', 'Session Id'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    # input missing operation parameters
    def fill(self, params={}):
        if params.has_key('sessionid') == False or params['sessionid'] == '':
            params.update({'sessionid':raw_input('Enter Session Id: ')})

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <kill-session>\n\
    <session-id>%s</session-id>\n\
  </kill-session>\n\
</rpc>\n" % (params['messageid'], params['sessionid'])

        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<ok' not in params['recvmsg']:
            print 'RPC <kill-session> failed:'
            print params['recvmsg']
        params.update({'writemsg':''})

    def writemsg(self, params={'writemsg':''}):
        pass


