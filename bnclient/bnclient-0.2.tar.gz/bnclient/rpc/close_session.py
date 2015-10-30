# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class close_session (object):
    def __init__(self, opts={}):
        self._dOptions = {}
        opts.update(self._dOptions)

#    def getopts(self):
#        return self._dOptions

    def fill(self, params={}):
        return

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <close-session/>\n\
</rpc>\n" % params['messageid']
        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<ok' not in params['recvmsg']:
            print 'RPC <close-session> failed:'
            print params['recvmsg']
        params.update({'writemsg':''})

    def writemsg(self, params={'writemsg':''}):
        pass
        sys.exit()


